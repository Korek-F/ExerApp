# TrainYourBrain
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Project guide](#project-guide)
* [Setup](#setup)

## General info
Online test creator with sessions and automatic
checking of test answers. Every app in the project is
supported by tests. 


## Technologies
* Django
* Htmx
* Java Script


## Project Guide
1. Go to http://localhost:8000.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc1.png)
2. Click "Sign up" and create a profile.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc2.png)
3. Login.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc3.png)
4. Now you are logged.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc4.png)
5. You can search for a specific test.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc5.png)
6. Type your answers.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc6.png)
7. Check your answers.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc7.png)
8. You can also create your own exercise set.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc8.png)
9. Now you can add content. Click "Edit".
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc9.png)
10. You can create exercise using 4 type of fields (Text, Blank, ABCD, Hint).
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc10.png)
11. You can see your progress in Preview.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc11.png)
12. After that, save your exercise.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc12.png)
13. Create more exercises.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc13.png)
14. Add categories for your exercise set.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc14.png)
15. Now your set is ready.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc15.png)
16. You can test it.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc16.png)
17. You can create scheduled exam. Click "Create Exam".
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc17.png)
18. Enter name, description, start and end time.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc18.png)
19. Remember, end time should be later thant start time.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc19.png)
20. You can copy link to exam and send it to your students.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc20.png)
21. This is session view.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc21.png)
22. If end time is set, users have to wait to see results.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc22.png)
23. After end time results are avaiable.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc23.png)
24. You can manage your students sessions on "Exam list". Click details to see Exam details.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc24.png)
25. Now you can see all your exam sessions.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc25.png)
26. You can check every session answers.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc26.png)
27. You can also find exercise set by category.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc27.png)
28. Every category has own view.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc28.png)
29. At the end, you can log out.
![app_img](https://github.com/Korek-F/ExerApp/blob/main/ExerApp/static/img/sc30.png)

## Setup
* python3 -m venv virt
* source venv/scripts/activate
* pip install -r requirements.txt
* cd InvGen
* python manage.py migrate 
* python manage.py runserver