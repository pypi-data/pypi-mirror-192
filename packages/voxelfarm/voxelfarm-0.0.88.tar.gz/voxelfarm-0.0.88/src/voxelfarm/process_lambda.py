import os
import time
import voxelfarm
from voxelfarm import voxelfarmclient

class process_lambda_framework:

    def __init__(self):  
        pass

    def input_string(self, id, label, default = ""):
        return ""

    def log(self, message):
        pass

    def progress(self, progress, message):
        pass

    def get_scrap_folder(self):
        return ""

    def get_tools_folder(self):
        return ""

    def get_entity_folder(self, id = None):
        return ""

    def download_entity_files(self, id = None):
        return ""

    def download_entity_file(self, filename, id = None):
        return ""

    def attach_file(self, filename, id = None):
        pass

    def attach_folder(self, folder, id = None):
        pass

    def upload(self, filename, name, id = None):
        pass

    def set_exit_code(self, code):
        pass

    def get_entity(self, id = None):
        return None

    def get_entity_file_list(self, id = None):
        return []

    def export_file(self, local_file_location, drop_zone_file_location):
        pass

    def get_callback_update_type(self):
        return ""

    def get_callback_entity_id(self):
        return ""

    def get_callback_entity_state(self):
        return ''
    
    def get_vf_api(self):
        return 'http://localhost'
    
    def increment_counter(self, counter, offset = 1):
        return 0
    
    def decrement_counter(self, counter, offset = 1):
        return 0

    def set_counter(self, counter, value = 0):
        pass

    def get_working_dir(self):
        return ''

    def swarm_db_upload(self, entity_id, folder, name, title):
        pass

class process_lambda_host:

    def __init__(self, framework = None):  
        if framework:
            self.lambda_framework = framework
        else:
            if voxelfarm.voxelfarm_framework:
                self.lambda_framework = voxelfarm.voxelfarm_framework
            else:
                self.lambda_framework = process_lambda_framework()

        vf_api_url = self.lambda_framework.get_vf_api()
        self.vf_api = voxelfarmclient.rest(vf_api_url)

    def input_string(self, id, label, default = ""):
        return self.lambda_framework.input_string(id, label, default)

    def log(self, message):
        self.lambda_framework.log(message)

    def progress(self, progress, message):
        self.lambda_framework.progress(progress, message)

    def get_scrap_folder(self):
        return self.lambda_framework.get_scrap_folder()

    def get_tools_folder(self):
        return self.lambda_framework.get_tools_folder()

    def get_entity_folder(self, id = None):
        return self.lambda_framework.get_entity_folder(id)

    def download_entity_files(self, id = None):
        return self.lambda_framework.download_entity_files(id)

    def download_entity_file(self, filename, id = None):
        return self.lambda_framework.download_entity_file(filename, id)

    def attach_file(self, filename, id = None):
        self.lambda_framework.attach_file(filename, id)

    def attach_folder(self, folder, id = None):
        self.lambda_framework.attach_folder(folder, id)

    def upload(self, filename, name, id = None):
        self.lambda_framework.Upload(filename, name, id)

    def set_exit_code(self, code):
        self.lambda_framework.set_exit_code(code)

    def get_entity(self, id = None):
        return self.lambda_framework.get_entity(id)

    def get_entity_file_list(self, id = None):
        return self.lambda_framework.get_entity_file_list(id)

    def export_file(self, local_file_location, drop_zone_file_location):
        return self.lambda_framework.export_file(local_file_location, drop_zone_file_location)

    def get_callback_update_type(self):
        return self.lambda_framework.get_callback_update_type()

    def get_callback_entity_id(self):
        return self.lambda_framework.get_callback_entity_id()

    def get_callback_entity_state(self):
        return self.lambda_framework.get_callback_entity_state()
    
    def increment_counter(self, counter, offset = 1):
        return self.lambda_framework.increment_counter(counter, offset)
    
    def decrement_counter(self, counter, offset = 1):
        return self.lambda_framework.decrement_counter(counter, offset)

    def set_counter(self, counter, value = 0):
        self.lambda_framework.set_counter(counter, value)

    def get_file_path(self, file):
        if os.path.exists(file):
            return file
        else:
            script_dir = self.lambda_framework.get_working_dir()
            self.lambda_framework.log('file is a relative path')
            file_path = os.path.join(script_dir, file)

            if os.path.exists(file_path):
                return file_path
    
        return None

    def load_file(self, file):
        file_path = self.get_file_path(file)

        if os.path.exists(file_path):
            return open(file_path)
    
        return None

    def get_working_dir(self):
        return self.lambda_framework.get_working_dir()

    def create_view(self, project, folder, name, view_type, view_lambda, inputs, props):
        self.lambda_framework.log(f'create_view:name:{name}|view_type:{view_type}|view_lambda:{view_lambda}|inputs:{inputs}|props:{props}')

        if view_type == None:
            lambda_file = self.load_file(view_lambda)
            if lambda_file == None:
                return {'success': False, 'error_info': 'Lambda file not found'}

            result = self.vf_api.create_lambda_python(
                project=project, 
                type=self.vf_api.lambda_type.View,
                name=name, 
                fields={
                    'file_folder': folder,
                    'virtual': '1'
                },
                code=lambda_file.read())
            if not result.success:
                return {'success': False, 'error_info': result.error_info}
            view_type = result.id

        input_fields = {
                'file_folder' : folder,
                'view_type' : view_type,
                'virtual' : '1',
                'state' : 'COMPLETE',
                'color_legend_attribute' : '',
                'color_legend_attribute_index' : '-1',
                'color_legend_gradient' : 'isoluminant_cgo_70_c39_n256',
                'color_legend_interpolate_gradient' : '1',
                'color_legend_mode' : '2',
                'color_legend_range_max' : '100',
                'color_legend_range_min' : '0',
                'color_legend_range_step' : '1',
                'color_legend_reverse_gradient' : '0',
                'file_date' : str(1000 * int(time.time())),
                'file_type' : 'VIEW',
                'input_filter_colors' : '0',
                'input_filter_e' : '8',
                'input_filter_normals' : '0',
                'input_label_colors' : 'Use Ortho-imagery',
                'input_label_e' : 'Terrain',
                'input_label_normals' : 'Use high resolution detail',
                'input_type_colorlegend' : '7',
                'input_type_colors' : '6',
                'input_type_e' : '3',
                'input_type_normals' : '6',
                'input_value_colors' : '0',
                'input_value_normals' : '0',         
            }
            
        for key in inputs:
            input_fields['input_value_' + key] = inputs[key]

        for key in props:
            input_fields[key] = props[key]
            
        result = self.vf_api.create_entity_raw(
            project=project,
            type=self.vf_api.entity_type.View,
            name=name,
            fields=input_fields,
            crs={}
        )

        if not result.success:
            return {'success': False, 'error_info': result.error_info}
        view_object = result.id
        
        self.lambda_framework.log(f'created_view:name:{name}|view_object:{view_object}')

        result = self.vf_api.create_entity_raw(
            project=project,
            type=self.vf_api.entity_type.View,
            name=name,
            fields={
                'file_folder' : folder,
                'view_type' : 'container',
                'state' : 'COMPLETE',
                'entity_container' : view_object
            },
            crs={}
        )

        if not result.success:
            return {'success': False, 'error_info': result.error_info}
        return {'success': True, 'id': result.id, 'error_info': 'None'}

    def create_report(self, project, folder, name, report_lambda, region, lod, inputs, fields = None, update_type = None):
        lambda_file = self.load_file(report_lambda)
        if lambda_file == None:
            return {'success': False, 'error_info': 'Lambda file not found'}
        
        result = self.vf_api.create_lambda_python(
            project=project, 
            type=self.vf_api.lambda_type.Report,
            name=f"Lambda for: {name}", 
            fields={
                'virtual': '1',
                'file_folder': folder
            },
            code=lambda_file.read())
        
        if not result.success:
            return {'success': False, 'error_info': result.error_info}
        
        report_lambda_id = result.id

        if fields == None:
            fields = {}

        fields['file_folder'] = folder

        entity = self.lambda_framework.get_entity()
        entity_id = entity["ID"]

        if update_type:
            fields['callback_update_type'] = entity_id + "/" + update_type

        result = self.vf_api.create_report(
            project=project, 
            program=report_lambda_id, 
            region=region,
            lod=str(lod),
            name=name, 
            fields=fields,
            inputs=inputs)
        
        if not result.success:
            return {'success': False, 'lambda_id': report_lambda_id, 'error_info': result.error_info}
        
        return {'success': True, 'id': result.id, 'lambda_id': report_lambda_id, 'error_info': 'None'}

    def create_lambda(self, project, folder, name, type, lambda_code):
        lambda_file = self.load_file(lambda_code)
        if lambda_file == None:
            return {'success': False, 'error_info': 'Lambda file not found'}

        result = self.vf_api.create_lambda_python(
            project=project, 
            type=type,
            name=name, 
            fields={
                'file_folder': folder
            },
            code=lambda_file.read())
        
        if not result.success:
            return {'success': False, 'error_info': result.error_info}
        
        report_lambda_id = result.id
        return {'success': True, 'id': report_lambda_id}

    def create_export(self, project, folder, name, export_lambda, region, lod, inputs, fields = None, update_type = None):
        lambda_file = self.load_file(export_lambda)
        if lambda_file == None:
            return {'success': False, 'error_info': 'Lambda file not found'}

        result = self.vf_api.create_lambda_python(
            project=project, 
            type=self.vf_api.lambda_type.Report,
            name="Export Lambda for " + name, 
            fields={
                'virtual': '1',
                'file_folder': folder
            },
            code=lambda_file.read())
        if not result.success:
            return {'success': False, 'error_info': result.error_info}
        report_lambda_id = result.id

        if fields == None:
            fields = {}

        fields['file_folder'] = folder
        fields['export_type'] = 'mesh'

        entity = self.lambda_framework.get_entity()
        entity_id = entity["ID"]

        if update_type:
            fields['callback_update_type'] = entity_id + "/" + update_type

        result = self.vf_api.create_export(
            project=project, 
            program=report_lambda_id, 
            region=region,
            lod=str(lod),
            name=name, 
            fields=fields,
            inputs=inputs)

        if not result.success:
            return {'success': False, 'lambda_id': report_lambda_id, 'error_info': result.error_info}

        return {'success': True, 'id': result.id, 'lambda_id': report_lambda_id, 'error_info': 'None'}

    def upload_db(self, entity_id, folder, name, title):
        return self.lambda_framework.upload_db(entity_id, folder, name, title)
