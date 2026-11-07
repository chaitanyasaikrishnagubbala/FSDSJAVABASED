
package com.rental.controller;

import com.rental.dao.UserDAO;
import com.rental.model.User;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import org.mindrot.jbcrypt.BCrypt;
import java.io.IOException;

@WebServlet("/register")
public class RegisterServlet extends HttpServlet {

    private final UserDAO userDAO=new UserDAO();

    @Override
    protected void doPost(HttpServletRequest request,HttpServletResponse response)
            throws ServletException,IOException {

        request.setCharacterEncoding("UTF-8");

        String name=request.getParameter("name");
        String email=request.getParameter("email");
        String password=request.getParameter("password");

        if(name==null||email==null||password==null||
           name.isBlank()||email.isBlank()||password.length()<8) {
            request.setAttribute("error","Enter valid details. Password must contain at least 8 characters.");
            request.getRequestDispatcher("/register.jsp").forward(request,response);
            return;
        }

        email=email.trim().toLowerCase();

        if(userDAO.getUserByEmail(email)!=null) {
            request.setAttribute("error","Email is already registered.");
            request.getRequestDispatcher("/register.jsp").forward(request,response);
            return;
        }

        User user=new User();
        user.setName(name.trim());
        user.setEmail(email);
        user.setPassword(BCrypt.hashpw(password,BCrypt.gensalt()));
        user.setRole("USER");

        if(userDAO.registerUser(user)) {
            response.sendRedirect(request.getContextPath()+"/login.jsp?registered=1");
        } else {
            request.setAttribute("error","Registration failed. Please try again.");
            request.getRequestDispatcher("/register.jsp").forward(request,response);
        }
    }
}
