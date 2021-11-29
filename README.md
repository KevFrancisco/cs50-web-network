# CS50 Web - Network

A light social media web application where users can make posts, like posts, and follow other users!
Majority of the sites functionality is done via a very simple API built in Django.
The site then fetches and updates data asynchronously, all done in native Javascript.

### Features:
- Users can make social 'posts'.
- Users can like their own, and other peoples' posts.
- Count of the number of likes a post has.
- If a user owns a post, they are able to 'Edit' or 'Delete' their own post.
- Clicking a user's name takes you to a 'Profile' page.
- Profile page displays all the user's post.
- The Profile page also allows a user to follow another user.
- If a user has followers or is following anyone, the Profile page will display them too.

---

### Update:
Moved to cloudinary for media file hosting.
See this tutorial for reference:
https://www.section.io/engineering-education/uploading-images-to-cloudinary-from-django-application/
