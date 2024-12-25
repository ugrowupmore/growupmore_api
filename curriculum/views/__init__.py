
from .subject import SubjectViewSet
from .chapter import ChapterViewSet
from .topic import TopicViewSet
from .subtopic import SubTopicViewSet
from .course_category import CourseCategoryViewSet
from .course_subcategory import CourseSubCategoryViewSet
from .course import CourseViewSet
from .module import ModuleViewSet
from .syllabus import SyllabusViewSet


__all__ = [
    "SubjectViewSet",
    "ChapterViewSet",
    "TopicViewSet",
    "SubTopicViewSet",
    "CourseCategoryViewSet",
    "CourseSubCategoryViewSet",
    "CourseViewSet",
    "ModuleViewSet",
    "SyllabusViewSet",
]