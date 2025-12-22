def get_weekday():
    from datetime import datetime
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    
    now = datetime.now()
    weekday_index = now.weekday()
    
    weekdays = [
        PkTexts.MONDAY,
        PkTexts.TUESDAY, 
        PkTexts.WEDNESDAY,
        PkTexts.THURSDAY,
        PkTexts.FRIDAY,
        PkTexts.SATURDAY,
        PkTexts.SUNDAY
    ]
    
    return weekdays[weekday_index] 