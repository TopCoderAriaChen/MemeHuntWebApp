# Meme Hunt Web Application

## Group Project for CITS5505 Agile Web Development

### Table of Contents

* [Introduction](#introduction)
* [Getting Started](#getting-started)
* [Project Overview](#project-overview)
* [Main Pages and Key Features](#main-pages-and-key-features)
* [Group Members](#group-members)
* [Technology Stack and Credits](#technology-stack-and-credits)
* [Source &amp; Credits](#source--credits)
* [License](#license)


## Introduction

**Meme Hunt** is a dynamic online platform that encourages users to explore, create, and share memes. It fosters a vibrant community where laughter and creativity merge to deliver joy and engagement through memes.


## Getting Started

### Prerequisites

* Python 3.9
* Flask
* SQLite3


### Installation

1. **Set up the database**:

    Before setting up the database, ensure that the `config.py` file is configured for the desired database system. The file contains configurations for both MySQL and SQLite. 

    **For MySQL:**

    ```python
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:PASSWORD@127.0.0.1:3306/DATABASE_NAME?charset=utf8mb4"
    ```

    **For SQLite:**

    ```python
    SQLALCHEMY_DATABASE_URI = "sqlite:///path_to_your_database.db"
    ```

    **After configuring** `config.py`​ **, execute the following commands to set up the database:**

    ```bash
    python3 config.py  # This script should include logic to initialize the database
    ```

    **Connect to the database for interactive command-line access：**

    ```bash
    sqlite3 db.sqlite
    ```
2. **Create and activate a virtual environment**:

    For Windows/Mac:

    ```bash
    python3.9 -m venv .venv
    .venv\Scripts\activate  # Windows
    source .venv/bin/activate  # macOS/Linux
    ```
3. **Install requirements**:

    ```bash
    pip install -r requirements.txt
    ```
4. **Run the application**:

    ```bash
    flask run
    ```
5. **Access the application**:

    Navigate to [http://127.0.0.1:5000/introductory](http://127.0.0.1:5000/introductory) in your web browser to access the introductory page



## Project Overview

* **Client**: Meme enthusiasts.
* **Project Purpose**: To provide a platform for meme lovers to share and interact with content, enhancing community engagement through digital creativity.
* **User Roles**:

  * **Meme Creators**: Users who create and post memes.
  * **Active Responders**: Users who participate by responding to meme requests with creations or suggestions.
  * **Community Engagers**: Users who interact with memes through likes, comments, and shares.
* **Features**:

  * Meme sharing and creation
  * Real-time interaction with posts
  * User-generated meme requests
  * Leaderboards based on user engagement


## Main Pages and Key Features

### **Authentication Pages**

* **Login and Register**: Secure entry points for users to access their accounts or create new ones.

### **Home Page**

* **Overview**: The main landing page that welcomes users, providing initial information and direct access to major functions like login or register.

### **About Us**

* **Purpose**: Introduces the application, detailing its goals, functionality, and the developers behind it.

### **User Profile**

* **Features**:

  * **Edit Profile**: Allows users to update personal information such as usernames and emails.
  * **Display Points and Rank**: Shows current points and user level, with incremental levels for every 500 points earned.

### **Dashboard Page**

* **Central Hub**: After login, this page acts as the central hub for user activities, including:

  * **Credit Rank**: Displays a leaderboard of users based on their earned credits to encourage active participation.
  * **My Posts**: Users can view and manage their posts.
  * **My Comments**: Users can view all comments they've made on different posts.
  * **Post Detail**: Detailed views of posts where users can see replies, allocate rewards, and interact with content.
  * **Filter of Meme Categories**: Allows users to filter posts based on specific meme categories.
  * **All Categories**: Shows posts across all categories.
  * **Search Feature**: Enables users to search for posts by keywords or tags.

### **New Post Page**

* **Functionality**: Users can request specific memes by creating a new post. This includes writing a title for the request, a description, and offering reward points for satisfactory responses.

### **Post Detail Page**

* **Features**:

  * **Response Options**: Users can reply with memes, text, and so on. Post creators can reward these responses by allocating a percentage of the total promised credits (ranging from 0% to 100%).
  * **Post Attributes**: Includes post time, author, meme category, total credits offered, and view count.

### **Search and Filter Functionality**

* **Search Posts**: Features a search bar for users to find specific posts.
* **Filter Posts**: Users can filter posts based on categories to streamline their browsing experience.

### **Community Engagement**

* **Leaderboards and Rankings**: Encourages competition and participation through visible rankings based on user activity.


## Group Memeber

| **UWA ID** | **Name** | **Github Username** |
| -- | -- | -- |
| **23750537** | **Yuanxi Chen** | **yuanxichennn** |
| **23618522** | **Aria Chen** | **TopCoderAriaChen** |
| **23914274** | **Raunak Chhabra** | **raunakchhabra** |
| **23789274** | **Ting Chen** | **TingChen-TC** |


## Technology Stack and Credits

### Built With

* **Frontend**:

  * **HTML5 &amp; CSS3**
  * **Bootstrap 4**
  * **JavaScript and jQuery**
  * **Font Awesome 5**

### Backend

* **Flask**
* **SQLite3**


## Source & Credits

* **Bootstrap 4**
* **Google Fonts**
* **Font Awesome 5**
* **jQuery Library**
* **W3C Validation Service**


## License

This project is licensed under the MIT license.
