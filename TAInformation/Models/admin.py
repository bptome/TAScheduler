from TAInformation.Models.user import User


class UserAdmin(User):

    # precondition: none
    # post condition: return an array of all Courses
    def display_courses(self):
        all_courses = Course.objects.all()
        course_content = []
        for course in all_courses:
            course_content.append(course.course_name)
        return course_content

    # precondition: none
    # post condition: return a String array of all people and their public and private info
    def display_people(self):
        # testing how this works
        all_users = User.objects.all()
        user_content = []
        for user in all_users:
            user_content.append(user.name)
        return user_content
