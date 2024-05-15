import argparse
import os
import re
import pandas

def print_and_log(log_file, message_string):
    print(message_string)
    log_file.write(message_string + '\n')

    return

#TODO: строго и правильно составить регулярку
def extract_tag_content(source_string, tag):
    if tag == 'LastCalculationGrandTotal':
        return re.findall('<' + tag + ' Chg="false">(.*?)</' + tag + '>', source_string, flags = re.DOTALL)
        
    return re.findall('<' + tag + '>(.*?)</' + tag + '>', source_string, flags = re.DOTALL)
    
def get_tag_value(source_string, tag_name, tag_list_index):
    tag_content = extract_tag_content(source_string, tag_name)
    
    tag_value = 'NULL'
    if len(tag_content) > 0: tag_value = tag_content[tag_list_index]

    return tag_value
    
def get_tag_multivalue(source_string, list_tag, lb_num, feature_tag, value_tag):
    list_blocks = extract_tag_content(source_string, list_tag)        
    if len(list_blocks) == 0:
        return 'NULL', -1
    
    file_fv_list = []
    
    selected_list_block = list_blocks[0 if lb_num == 'first' else -1]
    
    feature_blocks = extract_tag_content(selected_list_block, feature_tag)
    for fb in feature_blocks:
        feature_values = extract_tag_content(fb, value_tag)
        
        if len(feature_values) > 0:
            selected_feature_value = feature_values[0] #first            
            file_fv_list.append(selected_feature_value)
            
    return '[' + ', '.join(file_fv_list) + ']', len(file_fv_list)

def parse_claims_data(data_dir, log_file, parse_results, batch_size):
    log_file = open(log_file, 'w', encoding = 'utf-8')
    
    dir = [f for f in os.scandir(data_dir)]
    dir_len = len(dir)
    print_and_log(log_file, str(dir_len) + ' files found in ' + data_dir)
    
    subdirs = []
    for subdir_start_idx in range(0, dir_len, batch_size):
        subdir_end_idx = min(dir_len, subdir_start_idx + batch_size)
        #print(subdir_start_idx, subdir_end_idx)
        
        subdirs.append(dir[subdir_start_idx:subdir_end_idx])
        
    #print(subdirs)
    
    n = 0
    for subdir_num, sd in enumerate(subdirs):
        print_and_log(log_file, 'new batch started')
        
        claim_number_list = []
        vin_list = []
        manufacturer_list = []
        model_list = []
        sub_model_list = []
        color_list = []
        vehicle_kind_list = []
        part_desc_list, pdl_sizes = [], []
        rep_type_list, rtl_sizes = [], []
        mileage_list = []
        lcgt_list = []
        
        for file_number, file in enumerate(sd):
            #n = file_number + 1
            n = n + 1
            print_and_log(log_file, 'parsing file # ' +  str(n) + ': ' + file.name)
           
            file_content = open(file.path, 'r', encoding = 'utf-8').read()
            #print(file_content)
            
            claim_number = get_tag_value(file_content, 'ClaimNumber', 0)
            vin = get_tag_value(file_content, 'VIN', 0)
            manufacturer = get_tag_value(file_content, 'ManufacturerName', 0)
            model = get_tag_value(file_content, 'ModelName', 0)
            sub_model = get_tag_value(file_content, 'SubModelName', -1)
            color = get_tag_value(file_content, 'Color', 0)
            vehicle_kind = get_tag_value(file_content, 'VehicleKind', 0)
            part_desc, pds = get_tag_multivalue(file_content, 'PartDtls', 'first', 'PartDtl', 'PartDesc')
            rep_type, rts = get_tag_multivalue(file_content, 'PartDtls', 'first', 'PartDtl', 'RepTyp')
            mileage = get_tag_value(file_content, 'Mileage', 0)
            lcgt = get_tag_value(file_content, 'LastCalculationGrandTotal', 0)
            
            print_and_log(log_file, '\tClaimNumber: ' + claim_number)
            print_and_log(log_file, '\tVIN: ' + vin)
            print_and_log(log_file, '\tManufacturerName: ' + manufacturer)
            print_and_log(log_file, '\tModelName: ' + model)
            print_and_log(log_file, '\tSubModelName: ' + sub_model)
            print_and_log(log_file, '\tColor: ' + color)
            print_and_log(log_file, '\tVehicleKind: ' + vehicle_kind)
            print_and_log(log_file, '\t_Multi_PartDesc(' + str(pds) + '): ' + part_desc)
            print_and_log(log_file, '\t_Multi_RepTyp(' + str(rts) + '): ' + rep_type)
            print_and_log(log_file, '\tMileage: ' + mileage)
            print_and_log(log_file, '\tLastCalculationGrandTotal: ' + lcgt)
            
            claim_number_list.append(claim_number)
            vin_list.append(vin)
            manufacturer_list.append(manufacturer)
            model_list.append(model)
            sub_model_list.append(sub_model)
            color_list.append(color)
            vehicle_kind_list.append(vehicle_kind)
            part_desc_list.append(part_desc)
            pdl_sizes.append(pds)
            rep_type_list.append(rep_type)
            rtl_sizes.append(rts)
            mileage_list.append(mileage)
            lcgt_list.append(lcgt)
            
        #TODO: check that part_desc_list and rep_type_list are of same length!!!
        DF = pandas.DataFrame(data = {'ClaimNumber': claim_number_list, 'VIN': vin_list, 'ManufacturerName': manufacturer_list, 'ModelName': model_list, 'SubModelName': sub_model_list, 'Color': color_list, 'VehicleKind': vehicle_kind_list, '_Multi_PartDesc': part_desc_list, 'PartDescListSize': pdl_sizes, '_Multi_RepTyp': rep_type_list, 'RepTypListSize': rtl_sizes, 'Mileage': mileage_list, 'LastCalculationGrandTotal': lcgt_list})
        print('\nresult DataFrame:')
        print(DF)
        DF.to_excel(parse_results[:-5] + '_' + str(subdir_num + 1) + '.xlsx', sheet_name = 'claims_data', index = False)
        
    log_file.close()
    
    return

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        prog = 'Xml claim parser',
        description = 'Parse insurance claim data from Audatex .xml file'
    )
    
    arg_parser.add_argument(
        '--data_dir', 
        default = './xml_data/',
        help = 'location of .xml data files to parse'
    )
    arg_parser.add_argument(
        '--log_file', 
        default = './log.txt',
        help = 'file to write logs to'
    )
    arg_parser.add_argument(
        '--parse_results', 
        default = './claims_data.xlsx',
        help = 'file to write parse results to'
    )
    arg_parser.add_argument(
        '--batch_size', 
        type = int, 
        default = 10000,
        help = 'how many .xml files parse to single .xlsx file'
    )
    
    args = arg_parser.parse_args()
    print('\033[92m' + arg_parser.prog, args.__dict__, '\033[00m')
    
    assert os.path.isdir(args.data_dir), '--data_dir is not a valid directory'
    
    parse_claims_data(**args.__dict__)