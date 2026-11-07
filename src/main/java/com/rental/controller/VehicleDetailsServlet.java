
package com.rental.controller;

import com.rental.dao.VehicleDAO;
import com.rental.model.Vehicle;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet("/vehicle-details")
public class VehicleDetailsServlet extends HttpServlet {
    private final VehicleDAO vehicleDAO=new VehicleDAO();

    @Override
    protected void doGet(HttpServletRequest request,HttpServletResponse response)
            throws ServletException,IOException {

        String id=request.getParameter("id");

        try{
            int vehicleId=Integer.parseInt(id);
            Vehicle vehicle=vehicleDAO.getVehicleById(vehicleId);

            if(vehicle==null){
                response.sendError(HttpServletResponse.SC_NOT_FOUND,"Vehicle not found");
                return;
            }

            request.setAttribute("vehicle",vehicle);
            request.getRequestDispatcher("/vehicle-details.jsp").forward(request,response);

        }catch(NumberFormatException e){
            response.sendError(HttpServletResponse.SC_BAD_REQUEST,"Invalid vehicle ID");
        }
    }
}
