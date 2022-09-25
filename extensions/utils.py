from . import jalali
from django.utils import timezone
# def persian_number_converter(mystr):
 
#     numbers ={
#         "0":"۰",
#         "1":"۱" ,
#         "2":"۲" ,
#         "3":"۳" ,
#         "4":"۴",
#         "5":"۵" ,       =======برای فارسی نشان دادن تایم پست ها
#         "6":"۶" ,
#         "7":"۷",
#         "8":"۸" ,
#         "9":"۹" ,
        
#     } 
#     for e,p in numbers.items():
#         mystr = mystr.replace(e,p)
    
     
def jalali_converter(time):
    time=timezone.localtime(time)
    jmonths=["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
    
    time_to_str="{},{},{}".format(time.year,time.month,time.day)
    
    time_to_tuple=jalali.Gregorian(time_to_str).persian_tuple()
    
    time_to_list=list(time_to_tuple)
    
    for index, month in enumerate(jmonths):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break
    
    output="{} {} {},ساعت{}:{}".format(
            time_to_tuple[2],
            time_to_tuple[1],        
            time_to_tuple[0],
            time.hour,
            time.minute,
        ) 
    
    return   (output)

















   
#     return  persian_number_converter (output)













# def persian_number_converter(mystr):





#     numbers ={
        
#         "0":"۰",
#         "1":"۱" ,
#         "2":"۲" ,
#         "3":"۳" ,
#         "4":"۴",
#         "5":"۵" ,
#         "6":"۶" ,
#         "7":"۷",
#         "8":"۸" ,
#         "9":"۹" ,
        
#     } 
#     for e,p in numbers.items():
#      mystr = mystr.replace(e,p)

#     return mystr
# # ======برای فارسی نشان دادن تایم پست ها



# def converter(time):
#      jmonths=["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
     
#      time=timezone.localtime(time)
#     #  ===برای نشان دادن تایم دقیق پست ها
     
     
     
#      time_to_str="{},{},{}".format(time.year,time.month,time.day)
#      time_to_tuple=jalali.Gregorian(time_to_str).persian_tuple()
     
#      time_to_list=list(time_to_tuple)
     
#      for index, month in enumerate(jmonths):
#         if time_to_list[1] == index + 1:
#            time_to_list[1] = month
#            break
#     #  =====(کار نمیکند)برای نشان دادن سال های شمسی(بالاس)
      
#         output="{} {} {},ساعت{}:{}".format(
#             time_to_tuple[2],
#             time_to_tuple[1],        
#             time_to_tuple[0],
#             time.hour,
#             time.minute,
#         )     
#      return  persian_number_converter (output)

#     #  return  output)====برای انگلیسی نشان دادن تایم پست ها
    
#     #  return  persian_number_converter (output)======برای فارسی نشان دادن تایم پست ها