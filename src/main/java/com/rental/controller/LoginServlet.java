
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

@WebServlet("/login")
public class LoginServlet extends HttpServlet {
    private final UserDAO userDAO=new UserDAO();

    @Override
    protected void doPost(HttpServletRequest request,HttpServletResponse response)
            throws ServletException,IOException {

        request.setCharacterEncoding("UTF-8");

        String email=request.getParameter("email");
        String password=request.getParameter("password");

        if(email==null||password==null||email.isBlank()||password.isEmpty()){
            request.setAttribute("error","Enter your email and password.");
            request.getRequestDispatcher("/login.jsp").forward(request,response);
            return;
        }

        User user=userDAO.getUserByEmail(email.trim().toLowerCase());

        if(user==null||user.getPassword()==null||
                !BCrypt.checkpw(password,user.getPassword())){
            request.setAttribute("error","Invalid email or password.");
            request.getRequestDispatcher("/login.jsp").forward(request,response);
            return;
        }

        HttpSession oldSession=request.getSession(false);
        if(oldSession!=null){
            oldSession.invalidate();
        }

        HttpSession session=request.getSession(true);
        session.setAttribute("userId",user.getId());
        session.setAttribute("userName",user.getName());
        session.setAttribute("userRole",user.getRole());
        session.setMaxInactiveInterval(30*60);

        if("ADMIN".equalsIgnoreCase(user.getRole())){
            response.sendRedirect(request.getContextPath()+"/admin/dashboard");
        }else{
            response.sendRedirect(request.getContextPath()+"/vehicles");
        }
    }
}
