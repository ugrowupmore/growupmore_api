
# curriculum/views/course.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from authuser.permissions import IsEmployee

from curriculum.models.course import Course
from curriculum.serializers import CourseSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Courses",
        description="Retrieve a list of all courses.",
        responses={
            200: OpenApiResponse(
                response=CourseSerializer(many=True),
                description="A list of courses."
            )
        },
        tags=["Course"],
        examples=[
            OpenApiExample(
                name="Course List Response",
                summary="Successful retrieval of course list",
                description="Returns a list of all courses with their details.",
                value=[
                    {
                        "id": 1,
                        "code": "CS101",
                        "name": "Introduction to Computer Science",
                        "logo": "http://localhost:8000/media/courses_logos/cs101.png",
                        "level": "Beginner",
                        "price": "199.99",
                        "short_intro": "Basic concepts in computer science.",
                        "long_intro": "Comprehensive introduction covering algorithms, data structures, and programming basics.",
                        "video_url": "https://www.youtube.com/watch?v=course_example",
                        "tags": "computer science, algorithms, data structures, programming",
                        "description": "An introductory course to the fundamentals of computer science.",
                        "duration_days": 30,
                        "course_subcategory": 1,
                        "has_certification": True,
                        "prerequisite": "None",
                        "is_for": "Beginners interested in computer science.",
                        "will_learn": "Basic programming, problem-solving, algorithm design.",
                        "able_to": "Write simple programs, understand basic algorithms.",
                        "includes": "Video lectures, assignments, quizzes.",
                        "team": "Experienced CS educators.",
                        "roadmap": "http://localhost:8000/roadmaps/cs101",
                        "interview_checkpoints": "Coding challenges, theoretical exams.",
                        "apply_for": "Open enrollment.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-07-20T10:00:00Z",
                        "last_update_date": "2024-07-30T11:15:00Z",
                        "updated_by": None
                    },
                    # ... more courses
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Course Details",
        description="Retrieve detailed information about a specific course by its ID.",
        responses={
            200: OpenApiResponse(
                response=CourseSerializer,
                description="Detailed information about the course."
            ),
            404: OpenApiResponse(description="Course not found.")
        },
        tags=["Course"],
        examples=[
            OpenApiExample(
                name="Course Detail Response",
                summary="Successful retrieval of course details",
                description="Returns detailed information about a specific course.",
                value={
                    "id": 1,
                    "code": "CS101",
                    "name": "Introduction to Computer Science",
                    "logo": "http://localhost:8000/media/courses_logos/cs101.png",
                    "level": "Beginner",
                    "price": "199.99",
                    "short_intro": "Basic concepts in computer science.",
                    "long_intro": "Comprehensive introduction covering algorithms, data structures, and programming basics.",
                    "video_url": "https://www.youtube.com/watch?v=course_example",
                    "tags": "computer science, algorithms, data structures, programming",
                    "description": "An introductory course to the fundamentals of computer science.",
                    "duration_days": 30,
                    "course_subcategory": 1,
                    "has_certification": True,
                    "prerequisite": "None",
                    "is_for": "Beginners interested in computer science.",
                    "will_learn": "Basic programming, problem-solving, algorithm design.",
                    "able_to": "Write simple programs, understand basic algorithms.",
                    "includes": "Video lectures, assignments, quizzes.",
                    "team": "Experienced CS educators.",
                    "roadmap": "http://localhost:8000/roadmaps/cs101",
                    "interview_checkpoints": "Coding challenges, theoretical exams.",
                    "apply_for": "Open enrollment.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-20T10:00:00Z",
                    "last_update_date": "2024-07-30T11:15:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Course",
        description="Add a new course to the system by providing necessary details.",
        request=CourseSerializer,
        responses={
            201: OpenApiResponse(
                response=CourseSerializer,
                description="Course created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Course"],
        examples=[
            OpenApiExample(
                name="Course Creation Request",
                summary="Request body for creating a new course",
                description="Provide necessary fields to create a new course.",
                value={
                    "code": "CS102",
                    "name": "Data Structures",
                    "logo": "http://localhost:8000/media/courses_logos/cs102.png",
                    "level": "Intermediate",
                    "price": "299.99",
                    "short_intro": "In-depth study of data structures.",
                    "long_intro": "Advanced concepts in data structures, including trees, graphs, and hash tables.",
                    "video_url": "https://www.youtube.com/watch?v=data_structures_example",
                    "tags": "data structures, trees, graphs, algorithms",
                    "description": "A comprehensive course on various data structures and their applications.",
                    "duration_days": 45,
                    "course_subcategory": 1,
                    "has_certification": True,
                    "prerequisite": "Introduction to Computer Science",
                    "is_for": "Students and professionals seeking to deepen their understanding of data structures.",
                    "will_learn": "Implementation and analysis of complex data structures.",
                    "able_to": "Design efficient algorithms using advanced data structures.",
                    "includes": "Video lectures, coding assignments, projects.",
                    "team": "Expert data structure instructors.",
                    "roadmap": "http://localhost:8000/roadmaps/cs102",
                    "interview_checkpoints": "Algorithm design tasks, practical coding assessments.",
                    "apply_for": "Enrollment via the website.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Course Creation Success Response",
                summary="Successful course creation",
                description="Returns the created course details.",
                value={
                    "id": 2,
                    "code": "CS102",
                    "name": "Data Structures",
                    "logo": "http://localhost:8000/media/courses_logos/cs102.png",
                    "level": "Intermediate",
                    "price": "299.99",
                    "short_intro": "In-depth study of data structures.",
                    "long_intro": "Advanced concepts in data structures, including trees, graphs, and hash tables.",
                    "video_url": "https://www.youtube.com/watch?v=data_structures_example",
                    "tags": "data structures, trees, graphs, algorithms",
                    "description": "A comprehensive course on various data structures and their applications.",
                    "duration_days": 45,
                    "course_subcategory": 1,
                    "has_certification": True,
                    "prerequisite": "Introduction to Computer Science",
                    "is_for": "Students and professionals seeking to deepen their understanding of data structures.",
                    "will_learn": "Implementation and analysis of complex data structures.",
                    "able_to": "Design efficient algorithms using advanced data structures.",
                    "includes": "Video lectures, coding assignments, projects.",
                    "team": "Expert data structure instructors.",
                    "roadmap": "http://localhost:8000/roadmaps/cs102",
                    "interview_checkpoints": "Algorithm design tasks, practical coding assessments.",
                    "apply_for": "Enrollment via the website.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-31T16:40:00Z",
                    "last_update_date": "2024-07-31T16:40:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Course Details",
        description="Update information of an existing course by its ID.",
        request=CourseSerializer,
        responses={
            200: OpenApiResponse(
                response=CourseSerializer,
                description="Course updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Course not found.")
        },
        tags=["Course"],
        examples=[
            OpenApiExample(
                name="Course Update Request",
                summary="Request body for updating a course",
                description="Provide fields to update for the course.",
                value={
                    "price": "279.99",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Course Update Success Response",
                summary="Successful course update",
                description="Returns the updated course details.",
                value={
                    "id": 1,
                    "code": "CS101",
                    "name": "Introduction to Computer Science",
                    "logo": "http://localhost:8000/media/courses_logos/cs101.png",
                    "level": "Beginner",
                    "price": "279.99",
                    "short_intro": "Basic concepts in computer science.",
                    "long_intro": "Comprehensive introduction covering algorithms, data structures, and programming basics.",
                    "video_url": "https://www.youtube.com/watch?v=course_example",
                    "tags": "computer science, algorithms, data structures, programming",
                    "description": "An introductory course to the fundamentals of computer science.",
                    "duration_days": 30,
                    "course_subcategory": 1,
                    "has_certification": True,
                    "prerequisite": "None",
                    "is_for": "Beginners interested in computer science.",
                    "will_learn": "Basic programming, problem-solving, algorithm design.",
                    "able_to": "Write simple programs, understand basic algorithms.",
                    "includes": "Video lectures, assignments, quizzes.",
                    "team": "Experienced CS educators.",
                    "roadmap": "http://localhost:8000/roadmaps/cs101",
                    "interview_checkpoints": "Coding challenges, theoretical exams.",
                    "apply_for": "Open enrollment.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-20T10:00:00Z",
                    "last_update_date": "2024-08-07T19:30:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Course",
        description="Remove a course from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Course deleted successfully."),
            404: OpenApiResponse(description="Course not found.")
        },
        tags=["Course"],
        examples=[
            OpenApiExample(
                name="Course Deletion Success Response",
                summary="Successful course deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class CourseViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Course instances.
    """
    queryset = Course.objects.select_related(
        'course_subcategory__course_category'
    ).all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'code',
        'name',
        'level',
        'course_subcategory__course_category__category',
        'course_subcategory__sub_category',
        'has_certification',
        'status',
        'is_active'
    ]
    search_fields = ['code', 'name', 'tags']
    ordering_fields = ['code', 'name', 'level', 'course_subcategory__course_category__category',
                       'course_subcategory__sub_category', 'has_certification', 'status', 'is_active']
    ordering = ['code']
    permission_classes = [IsAuthenticated, IsEmployee]