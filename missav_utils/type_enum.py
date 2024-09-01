from enum import Enum


class MovieType(Enum):
    professional = 0
    fc2 = 1
    search = 2


class SortBy(Enum):
    ReleaseDate = 0
    RecentUpdate = 1
    TodayViews = 2
    WeeklyViews = 3
    MonthlyViews = 4
