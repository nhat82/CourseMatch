A website that UMD students can go on & see what courses/clubs their friends are in. Students can register, log in, and have a profile with enrolled/interested to enroll courses. Students can also have a following list and see what they are taking. Course listings pulls from planetterp API. Home Page can search for courses and people.

**Functionality will only be available to logged-in users**
- View their profile page
- Follow/unfollowing people
- Add a course they’re have enrolled or interested in
- See list of following people
- See list of courses

**Forms**
Register Form: Username, email, password
Login Form: Email, password
Follow Form: Used to follow/unfollow another user
Course Form: Used to add/remove a course

**Routes**
1. Landing page: main.py
    - `/index`
    - `/search`
2. Course: course.py
    - `/courses:` list all courses
    - `/course_name`: page for a course, show description.
        - if not logged in, wants to be enrolled/interested/taken → takes to register
4. User: User.py
    - `/user/<username>`:Profile page
    - `/user/<username>: List current user’s friends. List courses interested and enrolled.

**Stored/retrieved from MongoDB**
User
    - Username
    - Email
    - Password
    - Following
    - Courses
        - enrolled
        - interested
