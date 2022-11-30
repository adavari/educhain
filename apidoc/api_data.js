define({ "api": [
  {
    "type": "post",
    "url": "/api/v1/admin/login",
    "title": "AdminLogin",
    "name": "AdminLogin",
    "description": "<p>login admin user</p>",
    "group": "Admin",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>admin username.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>admin password.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "username",
          "content": "carret21",
          "type": "String"
        },
        {
          "title": "password",
          "content": "12terrac",
          "type": "String"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "Http/1.1 200 OK\n\n\n{\n    \"error\": false,\n    \"token\": \"eyads123ssdqw.asddfaQWEqwasdasfd213123qsdfas\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "controllers/v1/admin_controller.py",
    "groupTitle": "Admin"
  },
  {
    "type": "get",
    "url": "/api/v1/admin/course",
    "title": "GetAllCourseAdmin",
    "name": "GetAllCourseAdmin",
    "description": "<p>get all course with sections</p>",
    "group": "Admin",
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "Http/1.1 200 OK",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "controllers/v1/course_controller.py",
    "groupTitle": "Admin"
  },
  {
    "type": "get",
    "url": "/api/v1/admin/transaction",
    "title": "GetAllTransactions",
    "name": "GetAllTransactions",
    "description": "<p>get all transactions</p>",
    "group": "Admin",
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": " Http/1.1 200 OK\n\n[]",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "controllers/v1/user_controller.py",
    "groupTitle": "Admin"
  },
  {
    "type": "get",
    "url": "/api/v1/admin/user",
    "title": "GetAllUsers",
    "name": "GetAllUsers",
    "description": "<p>get all users</p>",
    "group": "Admin",
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": " Http/1.1 200 OK\n\n[]",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "controllers/v1/user_controller.py",
    "groupTitle": "Admin"
  },
  {
    "type": "post",
    "url": "/api/v1/admin/course",
    "title": "InsertNewCourse",
    "name": "InsertNewCourse",
    "description": "<p>insert new course</p>",
    "group": "Admin",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "title",
            "description": "<p>course title .</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "description",
            "description": "<p>course description.</p>"
          },
          {
            "group": "Parameter",
            "type": "int",
            "optional": false,
            "field": "price",
            "description": "<p>course price (if course is free insert 0).</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "teacher",
            "description": "<p>course teacher.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "title",
          "content": "the biggest frud",
          "type": "String"
        },
        {
          "title": "description",
          "content": "blockchain.",
          "type": "String"
        },
        {
          "title": "price",
          "content": "25000",
          "type": "int"
        },
        {
          "title": "teacher",
          "content": "unknown",
          "type": "String"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "Http/1.1 200 OK",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "controllers/v1/course_controller.py",
    "groupTitle": "Admin"
  },
  {
    "type": "post",
    "url": "/api/v1/admin/faq",
    "title": "InsertNewFaq",
    "name": "InsertNewFaq",
    "description": "<p>insert new frequently asked questions</p>",
    "group": "Admin",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "question",
            "description": "<p>faq question.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "answer",
            "description": "<p>faq answer.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "username",
          "content": "lerem ipsum? huh?",
          "type": "String"
        },
        {
          "title": "password",
          "content": "yep.",
          "type": "String"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "Http/1.1 200 OK",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "controllers/v1/faq_controller.py",
    "groupTitle": "Admin"
  },
  {
    "type": "post",
    "url": "/api/v1/admin/signup",
    "title": "SignupAdmin",
    "name": "SignupAdmin",
    "description": "<p>create new admin user</p>",
    "group": "Admin",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>admin username.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>admin password.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "username",
          "content": "carret21",
          "type": "String"
        },
        {
          "title": "password",
          "content": "12terrac",
          "type": "String"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "Http/1.1 200 OK\n\n\n{\n    \"error\": false,\n    \"message\": \"user created successfully\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "controllers/v1/admin_controller.py",
    "groupTitle": "Admin"
  },
  {
    "type": "get",
    "url": "/api/v1/admin/faq",
    "title": "GetAllFaqs",
    "name": "GetAllFaqs",
    "description": "<p>get all frequently asked questions</p>",
    "group": "Public",
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "Http/1.1 200 OK",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "controllers/v1/faq_controller.py",
    "groupTitle": "Public"
  },
  {
    "type": "post",
    "url": "/api/v2/auth/login",
    "title": "LoginUser",
    "name": "LoginUser",
    "description": "<p>login user with username and password</p>",
    "group": "Public",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>mobile number.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>user password</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "username",
          "content": "09121111111",
          "type": "String"
        },
        {
          "title": "password",
          "content": "ihatenodejs",
          "type": "String"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": " Http/1.1 200 OK\n\n\n{\n  \"error\": false,\n  \"token\": \"eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.IntcInNlc3Npb25cIjoge1wiaWRcIjogXCJiOGFjYTBkMS0wMTg1LTU3NzgtOTk5Ni1iYjMwZjc3NTkzMzhcIiwgXCJ1c2VyX2lkXCI6IFwiMDBmNWY1ZDEtYzQ0ZC01ZDBiLTg4NjMtZjBiODU4MmY2MGMxXCIsIFwiZGV2aWNlXCI6IFwicGNcIiwgXCJzdGF0dXNcIjogMSwgXCJmaXJlYmFzZV9pZFwiOiBudWxsLCBcImNyZWF0ZWRfYXRcIjogXCIyMDE5LTA2LTAzIDEyOjEwOjExLjY2MTg3NlwiLCBcInVwZGF0ZWRfYXRcIjogXCIyMDE5LTA2LTAzIDEzOjUyOjEzLjk1ODcyNFwiLCBcInBlbmRhcl90b2tlblwiOiBudWxsLCBcInVzZXJfYWdlbnRcIjogXCJQb3N0bWFuUnVudGltZS83LjYuMFwiLCBcInJlZl9jb2RlXCI6IFwiNjc0N1wifSwgXCJpYXRcIjogMTU1OTU1MzczMywgXCJleHBcIjogMTU1OTgxMjkzM30i.YDHztXZHiL-ZMRTaA9aQJCA09lxDR6uvwU6oq-688yO8uJOpmJYdIp7k9i50XWq067wbKC-L34waCDgovyvZ_MMxRLFSZco_983iCpMg43j4UCDb_SeLua5LwmmKHiR-EYYqg4jT8CTWDrWi5d8hFQpTbTuKUWmhSp6kjBcifhuSd4Necf_BkU7K2wliaysHbvbukbLqdBXC9BsjBpilczmEE24E1KkJeI5lF6F48R8eDPN0jS_lUZo_dMmuQq1p8BdTC6ZbWrxigO4e6JXif9nUj59Qoja6zJL9-rmVr7qywSH0FW2vGMyHHG207W1UzR2V7IcTC02dpab52yxs3g\"\n }",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "controllers/v2/auth_controller.py",
    "groupTitle": "Public"
  },
  {
    "type": "post",
    "url": "/api/v1/auth/otp",
    "title": "SendOTP",
    "name": "SendOTP",
    "description": "<p>Send Otp for user</p>",
    "group": "Public",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>mobile number.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>user password.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "username",
          "content": "09121111111",
          "type": "String"
        },
        {
          "title": "password",
          "content": "thisisahardpass",
          "type": "String"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "Http/1.1 200 OK\n\n\n{\n    \"error\": false,\n    \"message\": \"otp message sent\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "controllers/v1/auth_controller.py",
    "groupTitle": "Public"
  },
  {
    "type": "post",
    "url": "/api/v2/auth/signup",
    "title": "SignUp",
    "name": "SignUp",
    "description": "<p>signup user with username and password</p>",
    "group": "Public",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>mobile number.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>user password.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "username",
          "content": "09121111111",
          "type": "String"
        },
        {
          "title": "password",
          "content": "thisisahardpass",
          "type": "String"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "Http/1.1 200 OK\n\n\n{\n    \"error\": false,\n    \"message\": \"user created\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "controllers/v2/auth_controller.py",
    "groupTitle": "Public"
  },
  {
    "type": "post",
    "url": "/api/v1/auth/confirm",
    "title": "VerifyOtp",
    "name": "VerifyOTP",
    "description": "<p>verify otp</p>",
    "group": "Public",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>mobile number.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "code",
            "description": "<p>received code</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "username",
          "content": "09121111111",
          "type": "String"
        },
        {
          "title": "code",
          "content": "2345",
          "type": "String"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": " Http/1.1 200 OK\n\n\n{\n  \"error\": false,\n  \"token\": \"eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.IntcInNlc3Npb25cIjoge1wiaWRcIjogXCJiOGFjYTBkMS0wMTg1LTU3NzgtOTk5Ni1iYjMwZjc3NTkzMzhcIiwgXCJ1c2VyX2lkXCI6IFwiMDBmNWY1ZDEtYzQ0ZC01ZDBiLTg4NjMtZjBiODU4MmY2MGMxXCIsIFwiZGV2aWNlXCI6IFwicGNcIiwgXCJzdGF0dXNcIjogMSwgXCJmaXJlYmFzZV9pZFwiOiBudWxsLCBcImNyZWF0ZWRfYXRcIjogXCIyMDE5LTA2LTAzIDEyOjEwOjExLjY2MTg3NlwiLCBcInVwZGF0ZWRfYXRcIjogXCIyMDE5LTA2LTAzIDEzOjUyOjEzLjk1ODcyNFwiLCBcInBlbmRhcl90b2tlblwiOiBudWxsLCBcInVzZXJfYWdlbnRcIjogXCJQb3N0bWFuUnVudGltZS83LjYuMFwiLCBcInJlZl9jb2RlXCI6IFwiNjc0N1wifSwgXCJpYXRcIjogMTU1OTU1MzczMywgXCJleHBcIjogMTU1OTgxMjkzM30i.YDHztXZHiL-ZMRTaA9aQJCA09lxDR6uvwU6oq-688yO8uJOpmJYdIp7k9i50XWq067wbKC-L34waCDgovyvZ_MMxRLFSZco_983iCpMg43j4UCDb_SeLua5LwmmKHiR-EYYqg4jT8CTWDrWi5d8hFQpTbTuKUWmhSp6kjBcifhuSd4Necf_BkU7K2wliaysHbvbukbLqdBXC9BsjBpilczmEE24E1KkJeI5lF6F48R8eDPN0jS_lUZo_dMmuQq1p8BdTC6ZbWrxigO4e6JXif9nUj59Qoja6zJL9-rmVr7qywSH0FW2vGMyHHG207W1UzR2V7IcTC02dpab52yxs3g\"\n }",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "controllers/v1/auth_controller.py",
    "groupTitle": "Public"
  },
  {
    "type": "post",
    "url": "/api/v1/course/:course_id/buy",
    "title": "BuyCourse",
    "name": "BuyCourse",
    "description": "<p>buy course</p>",
    "group": "Secure",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>authorization token.</p>"
          }
        ]
      }
    },
    "parameter": {
      "examples": [
        {
          "title": "Authorization",
          "content": "bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.IntcInNlc3Npb25cIjoge1wiaWRcIjo",
          "type": "String"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "Http/1.1 200 OK\n\n{\n    \"url\" {\n        \"web_gate\" : \"www.zarinpal.com\",\n        \"zarin_gate\": \"www.zarinpal.com\",\n        \"mobile_gate\": \"www.zarinpal.com\"\n    },\n    \"transaction_id\": \"c35293a6-434b-4b4a-aab1-434eebefcd87\"\n    \n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "controllers/v1/course_controller.py",
    "groupTitle": "Secure"
  },
  {
    "type": "get",
    "url": "/api/v1/message",
    "title": "GetAllMessages",
    "name": "GetAllMessages",
    "description": "<p>get all user messages</p>",
    "group": "Secure",
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "Http/1.1 200 OK",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "controllers/v1/message_controller.py",
    "groupTitle": "Secure"
  },
  {
    "type": "get",
    "url": "/api/v1/course",
    "title": "GetUserCourses",
    "name": "GetUserCourses",
    "description": "<p>get user courses</p>",
    "group": "Secure",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>authorization token.</p>"
          }
        ]
      }
    },
    "parameter": {
      "examples": [
        {
          "title": "Authorization",
          "content": "bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.IntcInNlc3Npb25cIjoge1wiaWRcIjo",
          "type": "String"
        }
      ],
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "title",
            "description": "<p>course title .</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "Http/1.1 200 OK",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "controllers/v1/course_controller.py",
    "groupTitle": "Secure"
  },
  {
    "type": "get",
    "url": "/api/v1/auth/refresh",
    "title": "RefreshToken",
    "name": "RefreshToken",
    "description": "<p>refreshing token if token is expired</p>",
    "group": "Secure",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>authorization token.</p>"
          }
        ]
      }
    },
    "parameter": {
      "examples": [
        {
          "title": "Authorization",
          "content": "bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.IntcInNlc3Npb25cIjoge1wiaWRcIjo",
          "type": "String"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": " Http/1.1 200 OK\n\n\n{\n  \"error\": false,\n  \"token\": \"eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.IntcInNlc3Npb25cIjoge1wiaWRcIjogXCJiOGFjYTBkMS0wMTg1LTU3NzgtOTk5Ni1iYjMwZjc3NTkzMzhcIiwgXCJ1c2VyX2lkXCI6IFwiMDBmNWY1ZDEtYzQ0ZC01ZDBiLTg4NjMtZjBiODU4MmY2MGMxXCIsIFwiZGV2aWNlXCI6IFwicGNcIiwgXCJzdGF0dXNcIjogMSwgXCJmaXJlYmFzZV9pZFwiOiBudWxsLCBcImNyZWF0ZWRfYXRcIjogXCIyMDE5LTA2LTAzIDEyOjEwOjExLjY2MTg3NlwiLCBcInVwZGF0ZWRfYXRcIjogXCIyMDE5LTA2LTAzIDEzOjUyOjEzLjk1ODcyNFwiLCBcInBlbmRhcl90b2tlblwiOiBudWxsLCBcInVzZXJfYWdlbnRcIjogXCJQb3N0bWFuUnVudGltZS83LjYuMFwiLCBcInJlZl9jb2RlXCI6IFwiNjc0N1wifSwgXCJpYXRcIjogMTU1OTU1MzczMywgXCJleHBcIjogMTU1OTgxMjkzM30i.YDHztXZHiL-ZMRTaA9aQJCA09lxDR6uvwU6oq-688yO8uJOpmJYdIp7k9i50XWq067wbKC-L34waCDgovyvZ_MMxRLFSZco_983iCpMg43j4UCDb_SeLua5LwmmKHiR-EYYqg4jT8CTWDrWi5d8hFQpTbTuKUWmhSp6kjBcifhuSd4Necf_BkU7K2wliaysHbvbukbLqdBXC9BsjBpilczmEE24E1KkJeI5lF6F48R8eDPN0jS_lUZo_dMmuQq1p8BdTC6ZbWrxigO4e6JXif9nUj59Qoja6zJL9-rmVr7qywSH0FW2vGMyHHG207W1UzR2V7IcTC02dpab52yxs3g\"\n }",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "controllers/v1/auth_controller.py",
    "groupTitle": "Secure"
  },
  {
    "type": "post",
    "url": "/api/v1/message",
    "title": "SendNewMessage",
    "name": "SendNewMessage",
    "description": "<p>send new message (contact us)</p>",
    "group": "Secure",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "title",
            "description": "<p>message title.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "message",
            "description": "<p>message.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "title",
          "content": "hi :)",
          "type": "String"
        },
        {
          "title": "message",
          "content": "i'm stupid :)))",
          "type": "String"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "Http/1.1 200 OK",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "controllers/v1/message_controller.py",
    "groupTitle": "Secure"
  },
  {
    "type": "post",
    "url": "/api/v1/auth/unsub",
    "title": "Unsubscribe",
    "name": "Unsubscribe",
    "description": "<p>unsubscribe user</p>",
    "group": "Secure",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>authorization token.</p>"
          }
        ]
      }
    },
    "parameter": {
      "examples": [
        {
          "title": "Authorization",
          "content": "bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.IntcInNlc3Npb25cIjoge1wiaWRcIjo",
          "type": "String"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "   Http/1.1 200 OK\n\n\n{\n    \"error\": false,\n    \"message\": \"user disabled successfully\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "controllers/v1/auth_controller.py",
    "groupTitle": "Secure"
  },
  {
    "type": "post",
    "url": "/api/v1/payment/verify",
    "title": "VerifyTransaction",
    "name": "VerifyTransaction",
    "description": "<p>verify transaction</p>",
    "group": "Secure",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>authorization token.</p>"
          }
        ]
      }
    },
    "parameter": {
      "examples": [
        {
          "title": "Authorization",
          "content": "bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.IntcInNlc3Npb25cIjoge1wiaWRcIjo",
          "type": "String"
        }
      ],
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "transaction_id",
            "description": "<p>transaction id .</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "Http/1.1 200 OK\n\n{\n    \"error\": false, \"message\": \"payment is successfull\"            \n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "controllers/v1/course_controller.py",
    "groupTitle": "Secure"
  }
] });
