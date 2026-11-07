
package com.rental.controller;

import com.rental.dao.VehicleDAO;
import com.rental.model.Vehicle;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.util.List;

@WebServlet("/vehicles")
public class VehicleServlet extends HttpServlet {
    private final VehicleDAO vehicleDAO=new VehicleDAO();

    @Override
    protected void doGet(HttpServletRequest request,HttpServletResponse response)
            throws ServletException,IOException {

        List<Vehicle> vehicles=vehicleDAO.getAvailableVehicles();

        request.setAttribute("vehicles",vehicles);
        request.getRequestDispatcher("/vehicles.jsp").forward(request,response);
    }
}
