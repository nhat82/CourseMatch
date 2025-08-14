A website that UMD students can go on & see what courses/club their friends are in or interested in. Students can register, log in, and have a profile with enrolled/interested to enroll courses, clubs. Students can also have a following list and see what they are taking. Course listings pulls from planetterp API and TerpLink. Home Page can search for courses, clubs, and people.

### Functionality will only be available to logged-in users
- View their profile page
- Follow/unfollowing people
- Add courses, clubs they’re have enrolled or interested in
- See list of following people
- See list of courses

### Forms
1. Register Form: Username, email, password 
2. Login Form: Email, password 
3. Follow Form: Used to follow/unfollow another user
4. Course Form: Used to add/remove a course
5. Club Form: Used to add/remove a course

### Routes
1. Courses:
    - `/index`: Home Page
    - `/search-results/<query>`: Search Person (have to be exact username), Course by (department or specific course name)
    - `/course_name`: page for a course, show description. If not logged in, wants to be enrolled/interested/taken → takes to register
    - `/add_course/<course_name>`: form to add course to be interested/enrolled.
    - `/remove_course/<course_name>`: form to remove course from interested/enrolled.
    - `/courses/club/<club_name>`: page for a club, show description, link. If not logged in, wants to be enrolled/interested/taken → takes to register
    - `/add_club/<club_name>`: form to add club to be interested/enrolled.
    - `/remove_club/<club_name>`: form to remove club from interested/enrolled.
2. Users: 
    - `/register`: Register
    - `/login`: Login
    - `/logout`: Logout
    - `/account`: Current logged-in user's account details. Profile picture, Update username, profile picture forms. List users they are following, interested courses, enrolled courses, potential courses they might like based on the their following's courses. 
    - `/user/<username>`: Detail page of other user. List courses interested and enrolled. Show whether Following or not, show Follow/Unfollow button.

### Stored/retrieved from MongoDB
User:Username, Email, Password, Following, Courses(enrolled, interested)

### API
Pulls courses from Planetterp API, shows number of credits, prerequisites. Webscrapped using webdriver to get all clubs from TerpLink

## Video Demo Link: https://drive.google.com/file/d/1vvrA2Th76xeXRb6DBkaO1eRWZXd_Y6uy/view?usp=sharing

https://cmsc-388-j-final-course-match-uhsj.vercel.app/


## 🤝 Contributing

### Clone the repo

```bash
git clone https://github.com/xyz/zipzod@latest
cd zipzod
```

### Build the project

```bash
go build
```

### Run the project

```bash
./zipzod -i ./input -o ./output.zip
```

### Run the tests

```bash
go test ./...
```

### Submit a pull request

If you'd like to contribute, please fork the repository and open a pull request to the `main` branch.



