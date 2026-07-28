# Multi-Author Blogging Platform (Django)

A full-featured backend blogging platform built with Django. It supports role-based access control (Readers vs Authors vs Admin), category/tag organization, draft/published workflow, comments moderation, post likes, and an author analytics dashboard.

---

## 🚀 Features

- **User Roles & Auth:** Public reading, registered readers (comments/likes), promoted authors (content management), and site admins via Django Admin.
- **Post Management:** Category & Tag system, auto-generated unique slugs, featured image uploads, draft status visibility protection.
- **Author Dashboard:** Post status view, view counts tracking, like stats, and CRUD operations restricted to post authors.
- **Interactions:** One-like-per-user toggle system and owner/author/admin comment moderation.
- **Search & Pagination:** Case-insensitive search on title/content and filter by category/tag.

---

## 🛠️ Setup & Local Installation

### 1. Clone the Repository
```bash
git clone https://github.com/imranrisal-dev/multi_author_blog.gitgit remote add origin https://github.com/imranrisal-dev/multi_author_blog.git
cd multi_author_blog