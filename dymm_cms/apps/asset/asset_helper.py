import os, shutil, datetime, pytz
from werkzeug.utils import secure_filename

from dymm_cms.helpers.string_helpers import to_camel_case
from . import _u
from .asset_forms import AssetDirForm


class AssetHelper(object):
    # Generators
    # -------------------------------------------------------------------------
    @staticmethod
    def gen_matching_assets(png_names: list, license_dict: dict,
                            svg_dict: dict) -> list:
        assets = list()
        for png_name in png_names:
            asset = dict(png_name=png_name)
            try:
                name = png_name.split('.')
                key = name[0] + ".pdf"
                license_name = license_dict[key]
                asset["pdf_name"] = license_name
            except KeyError:
                asset["pdf_name"] = None
            try:
                name = png_name.split('.')
                key = name[0] + ".svg"
                svg_name = svg_dict[key]
                asset["svg_name"] = svg_name
            except KeyError:
                asset["svg_name"] = None
            assets.append(asset)
        return assets

    # Validators
    # -------------------------------------------------------------------------
    @staticmethod
    def is_allowed_file_type(filename: str, file_type):
        if not file_type == filename.split('.')[1]:
            return False
        return True

    @staticmethod
    def allowed_license_file(filename):
        allowed_extensions = ['pdf']
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions

    # Converters
    # -------------------------------------------------------------------------
    @staticmethod
    def convert_file_names_into_json(names: list) -> dict:
        json = dict()
        for name in names:
            json[name] = name
        return json

    @staticmethod
    def convert_file_names_into_app_code(names: list):
        gen_lines = list()
        for file_name in names:
            asset_name = file_name.split('.')[0]
            gen_line = "static let {0} = UIImage(named: \"{1}\")!".format(
                to_camel_case(asset_name, '-'), asset_name)
            gen_lines.append(gen_line)
        return gen_lines

    # Getters
    # -------------------------------------------------------------------------
    @staticmethod
    def get_asset_dir_names():
        names = list()
        (_, dirnames, _) = next(os.walk(_u.ASSET))
        names.extend(dirnames)
        names.sort()
        return names

    @staticmethod
    def get_file_names(dirname, target, reverse=False):
        names = list()
        if target == 'zip':
            location = "{0}/{1}".format(_u.ASSET, dirname)
        else:
            location = "{0}/{1}/{2}".format(_u.ASSET, dirname, target)
        (_, _, filenames) = next(os.walk(location))
        names.extend(filenames)
        names.sort(reverse=reverse)
        return names

    @staticmethod
    def get_dir_select_choices(dirnames):
        choices = []
        for dirname in dirnames:
            choice = (dirname, dirname)
            choices.append(choice)
        return choices

    @staticmethod
    def get_dir_form() -> AssetDirForm:
        form = AssetDirForm()
        return form

    @staticmethod
    def create_directory_zip(dirname, target):
        str_date = datetime.datetime.now(tz=pytz.utc).strftime('%Y%m%d-%H%M%S')
        root_dir = '{}/{}'.format(_u.ASSET, dirname)
        destination = '{}/{}'.format(_u.ASSET, 'archive')
        shutil.make_archive(
            '{}/{}-{}-{}'.format(destination, str_date, dirname, target),
            'zip',
            root_dir + "/" + target
        )
        return True

    # Create methods
    # -------------------------------------------------------------------------
    @staticmethod
    def upload_multi_files(files, dirname, file_type):
        cnt = 0
        for file in files:
            if file and AssetHelper.is_allowed_file_type(file.filename, 'png'):
                str_list = file.filename.split('.')
                try:
                    option = dirname.split('@')[1]
                    filename = "{0}@{1}.{2}".format(str_list[0], option,
                                                    str_list[1])
                except IndexError:
                    filename = secure_filename(file.filename)
                path = _u.ASSET + "/{0}/{1}".format(dirname, file_type)
                file.save(os.path.join(path, filename))
                cnt += 1
        return cnt

    @staticmethod
    def upload_single_file(file, location, filename):
        file.save(os.path.join(location, filename))
        return True

    # Update methods
    # -------------------------------------------------------------------------
    @staticmethod
    def rename_asset(dirname, old_name, new_name):
        targets = ['png', 'svg', 'pdf']
        for target in targets:
            location = "{}/{}/{}/".format(_u.ASSET, dirname, target)
            old_file = os.path.join(location, '{}.{}'.format(old_name, target))
            new_file = os.path.join(location, '{}.{}'.format(new_name, target))
            try:
                os.rename(old_file, new_file)
            except FileNotFoundError:
                continue
        return True

    @staticmethod
    def move_asset_dir(old_dir, new_dir, filename):
        old_dir = _u.ASSET + "/" + old_dir
        new_dir = _u.ASSET + "/" + new_dir
        file_set = ["/png/" + filename + ".png", "/pdf/" + filename + ".pdf",
                    "/svg/" + filename + ".svg"]
        for file_path in file_set:
            try:
                shutil.move(old_dir + file_path, new_dir + file_path)
            except OSError:
                continue
        return True

    # Delete methods
    # -------------------------------------------------------------------------
    @staticmethod
    def delete_asset(dirname, target, filename):
        if target == 'zip':
            _path = '{}/{}/{}.{}'.format(_u.ASSET, dirname, filename, target)
        else:
            _path = '{}/{}/{}/{}.{}'.format(_u.ASSET, dirname, target,
                                            filename, target)
        try:
            os.remove(_path)
        except FileNotFoundError:
            return False
        return True
