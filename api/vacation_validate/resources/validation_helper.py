def overlap_checker(v1, v2):
    start1 = v1.vacation_start
    start2 = v2.vacation_start
    end1 = v1.vacation_end
    end2 = v2.vacation_end
    latest_start = max(start1, start2)
    earliest_end = min(end1, end2)
    overlap = max(0, (earliest_end - latest_start).days + 1)
    return overlap


def overlapped_dates(vacations):
    overlaps = {}
    for i, vacation in enumerate(vacations[:-1]):
        for next_vacation in vacations[i + 1:]:
            overlap_days = overlap_checker(vacation, next_vacation)
            if overlap_days:
                overlaps[i] = {'ids': (vacation.id, next_vacation.id),
                               'days': overlap_days}
    return overlaps
