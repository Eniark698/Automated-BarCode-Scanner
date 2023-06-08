#select location
# , left(location,12) || '/f/' || substring(location,14,20) || right(location, length(location)-12) as new_path 
# from scantable 
# where dateandtime>='2023-06-07' and dateandtime<'2023-06-08';
# select count(*) from (select distinct on (id) id,barcode,location,dateandtime,storage_inbytes,BarCodeType,direction,is_rescanned from scantable)as qerry;з