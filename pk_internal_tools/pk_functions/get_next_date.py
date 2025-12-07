

def get_next_date(period, current_date):
    from datetime import timedelta
    import calendar

    if period == "daily":
        return current_date + timedelta(days=1)
    elif period == "weekly":
        return current_date + timedelta(days=7)
    elif period == "biweekly":
        return current_date + timedelta(days=14)
    elif period == "monthly":
        # 다음 달의 1일로 이동
        next_month = current_date.month + 1 if current_date.month < 12 else 1
        next_year = current_date.year + 1 if next_month == 1 else current_date.year
        return current_date.replace(year=next_year, month=next_month, day=1)
    elif period == "yearly":
        return current_date.replace(year=current_date.year + 1)
    elif period == "last_day_of_month":
        # 다음 달의 마지막 날로 이동
        next_month = current_date.month + 1 if current_date.month < 12 else 1
        next_year = current_date.year + 1 if next_month == 1 else current_date.year
        next_first_day = current_date.replace(year=next_year, month=next_month, day=1)
        last_day = calendar.monthrange(next_first_day.year, next_first_day.month)[1]
        return next_first_day.replace(day=last_day)
    else:
        raise ValueError(f"Unsupported period: {period}")
