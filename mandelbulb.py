import torch

def generate_mandelbulb(dim, power, iterations, threshold=2.0):
    #Use GPU or CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    #Generate 3D grid of points, range [-1.5, 1.5]
    lin = torch.linspace(-1.5, 1.5, dim, device = device)
    grid_points = torch.cartesian_prod(lin, lin, lin).float()
    
    mandelbulb_points = []
    zeta = torch.zeros_like(grid_points, device = device)
    r = torch.norm(grid_points, dim=1)

    for i in range(iterations):
        #Spherical coordinates
        r = torch.norm(zeta, dim = 1)
        
        #Check escaped points and reset them 
        escaped = r > threshold
        zeta[escaped] = 0
        
        theta = torch.atan2(torch.sqrt(zeta[:, 0]**2 + zeta[:, 1]**2), zeta[:, 2])
        phi = torch.atan2(zeta[:, 1], zeta[:, 0])

        #Mandelbulb transformation
        r_n = r**power
        sin_theta_n = torch.sin(theta * power)
        cos_theta_n = torch.cos(theta * power)
        cos_phi_n = torch.cos(phi * power)
        sin_phi_n = torch.sin(phi * power)

        #Compute the new x, y, z
        new_x = r_n * sin_theta_n * cos_phi_n
        new_y = r_n * sin_theta_n * sin_phi_n
        new_z = r_n * cos_theta_n

        #Update zeta
        zeta = torch.stack([new_x, new_y, new_z], dim=1).float() + grid_points
        
        #Check if the point is inside
        if i == iterations - 1:
            mask_inside = (r <= threshold)
            mandelbulb_points.append(grid_points[mask_inside])  #Add point
    
    mandelbulb_points = torch.cat(mandelbulb_points, dim=0).cpu()  #Convert to CPU tensor ([C,D]) C is count of points and D is the number of plot dimensions
    return mandelbulb_points