"""
Utility functions for aiida plugins.

Useful for:
 * compatibility with different aiida versions

"""
from __future__ import absolute_import

import aiida
from distutils.version import StrictVersion  # pylint: disable=no-name-in-module,import-error

AIIDA_VERSION = StrictVersion(aiida.get_version())


def load_verdi_data():
    """Load the verdi data click command group for any version since 0.11."""
    verdi_data = None
    import_errors = []

    try:
        from aiida.cmdline.commands import data_cmd as verdi_data
    except ImportError as err:
        import_errors.append(err)

    if not verdi_data:
        try:
            from aiida.cmdline.commands import verdi_data
        except ImportError as err:
            import_errors.append(err)

    if not verdi_data:
        try:
            from aiida.cmdline.commands.cmd_data import verdi_data
        except ImportError as err:
            import_errors.append(err)

    if not verdi_data:
        err_messages = '\n'.join(
            [' * {}'.format(_err) for _err in import_errors])
        raise ImportError(
            'The verdi data base command group could not be found:\n' +
            err_messages)

    return verdi_data


def load_dbenv_if_not_loaded():
    # pylint: disable=import-error
    if AIIDA_VERSION < StrictVersion('1.0a0'):
        from aiida.cmdline.dbenv_lazyloading import load_dbenv_if_not_loaded as fn
        return fn()

    from aiida.cmdline.utils.decorators import load_dbenv_if_not_loaded as fn
    return fn()


def extract_cif(infile, folder, nodes_export_subfolder="nodes", aiida_export_subfolder="aiida", silent=False):
    """
    Extract the nodes to be imported from a TCOD CIF file. TCOD CIFs,
    exported by AiiDA, may contain an importable subset of AiiDA database,
    which can be imported. This function prepares SandboxFolder with files
    required for import.

    :param infile: file path
    :param folder: a SandboxFolder, used to extract the file tree
    :param nodes_export_subfolder: name of the subfolder for AiiDA nodes
    :param aiida_export_subfolder: name of the subfolder for AiiDA data
        inside the TCOD CIF internal file tree
    :param silent: suppress debug print
    """
    # pylint: disable=unused-argument,too-many-locals,invalid-name
    from six.moves import urllib
    import CifFile
    from aiida.common.exceptions import ValidationError
    from aiida.common.files import md5_file, sha1_file
    from aiida.tools.dbexporters.tcod import decode_textfield

    values = CifFile.ReadCif(infile)
    values = values[list(values.keys())[0]]  # taking the first datablock in CIF

    for i in range(len(values['_tcod_file_id']) - 1):
        name = values['_tcod_file_name'][i]
        if not name.startswith(aiida_export_subfolder + os.sep):
            continue
        dest_path = os.path.relpath(name, aiida_export_subfolder)
        if name.endswith(os.sep):
            if not os.path.exists(folder.get_abs_path(dest_path)):
                folder.get_subfolder(folder.get_abs_path(dest_path), create=True)
            continue
        contents = values['_tcod_file_contents'][i]
        if contents in ['?', '.']:
            uri = values['_tcod_file_uri'][i]
            if uri is not None and uri != '?' and uri != '.':
                contents = urllib.request.urlopen(uri).read()
        encoding = values['_tcod_file_content_encoding'][i]
        if encoding == '.':
            encoding = None
        contents = decode_textfield(contents, encoding)
        if os.path.dirname(dest_path) != '':
            folder.get_subfolder(os.path.dirname(dest_path) + os.sep, create=True)
        with io.open(folder.get_abs_path(dest_path), 'w', encoding='utf8') as fhandle:
            fhandle.write(contents)
            fhandle.flush()
        md5 = values['_tcod_file_md5sum'][i]
        if md5 is not None:
            if md5_file(folder.get_abs_path(dest_path)) != md5:
                raise ValidationError("MD5 sum for extracted file '{}' is "
                                      "different from given in the CIF "
                                      "file".format(dest_path))
        sha1 = values['_tcod_file_sha1sum'][i]
        if sha1 is not None:
            if sha1_file(folder.get_abs_path(dest_path)) != sha1:
                raise ValidationError("SHA1 sum for extracted file '{}' is "
                                      "different from given in the CIF "
                                      "file".format(dest_path))