import threading
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import mandelbulb

def plot_mandelbulb(power=6, dim=40, iterations = 20, sample=10000):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    #Create sliders
    ax_power = plt.axes([0.25, 0.06, 0.65, 0.03])
    ax_dim = plt.axes([0.25, 0.03, 0.65, 0.03])
    ax_iterations = plt.axes([0.25, 0.09, 0.65, 0.03])

    slider_power = Slider(ax_power, "Power", 2, 20, valinit = power, valstep = 1)
    slider_dim = Slider(ax_dim, "Dimension", 10, 160, valinit = dim, valstep = 5)
    slider_iterations = Slider(ax_iterations, "Iterations", 1, 30, valinit = iterations, valstep = 1)

    global mandelbulb_points
    mandelbulb_points = None

    def update_plot(val):
        global mandelbulb_points

        #Get the input values
        power_value = int(slider_power.val)
        dim_value = int(slider_dim.val)
        iter_val = int(slider_iterations.val)

        def generate():
            global mandelbulb_points
            mandelbulb_points = mandelbulb.generate_mandelbulb(dim = dim_value, power = power_value, iterations = iter_val) #Calculate Mandelbulb points
            step = max(1, len(mandelbulb_points) // sample)

            #Clear the plot and generate a new one
            ax.clear()
            ax.scatter(
                mandelbulb_points[::step, 0],
                mandelbulb_points[::step, 1],
                mandelbulb_points[::step, 2],
                c = mandelbulb_points[::step, 2],  #Use z to determine the color
                cmap = "inferno",
                s = 0.5
            )
            ax.set_title(f"Mandelbulb (power = {int(power_value)}, dim = {dim_value}, iterations = {iter_val}, generated points = {len(mandelbulb_points)})")
            fig.canvas.draw_idle()

        threading.Thread(target = generate).start()

    #Initialize the plot
    update_plot(None)

    slider_power.on_changed(update_plot)
    slider_dim.on_changed(update_plot)
    slider_iterations.on_changed(update_plot)

    plt.show()

def main():
    plot_mandelbulb()

if __name__ == "__main__":
    main()