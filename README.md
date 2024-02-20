# INSTALLATION

1) with Make:

       make up

   
3) without make

        docker compose up / docker-compose up //if you get error on linux use `sudo` before command
   
# DOCUMENTATION

1) Authorization

   /api/v1/auth/users/ - create user (POST) or get list of users (GET). 
   
   example of request body (fields `work_place`, `role`, `is_superuser` are not required.):
   
        {
          "first_name": "",
          "last_name": "",
          "email": "",
          "password": "",
          "phone": "",
          "work_place": null,
          "role": null,
          "is_superuser": false
        }

   *. To get list of users you should be authorized as `is_staff` or `is_superuser` user.

  After posting new user you will get message to your email with activation link. Activation link look like this:

      
   
