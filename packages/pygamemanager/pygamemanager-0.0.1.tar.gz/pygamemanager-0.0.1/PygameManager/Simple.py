
try:
    import pygame
except ImportError:
    print("Pygame not found please install pygame by running 'pip install pygame' in your terminal")
except Exception as e:
    print("error while importing pygame: " + str(e))
    print("please remember to import pygame")







# Main class for Simple
class PygameManager:
    def __init__(self, update_, draw, events):
        self.update = update_
        self.draw = draw
        self.events = events
        self.width = 300
        self.height = 300
        self.background_colour = (234, 212, 252)
        self.title = "Simple Pygame Window"
    def setExtras(self, width=300, height=300, background_colour=(234, 212, 252), title="Simple Pygame Window"):
        self.width = width
        self.height = height
        self.background_colour = background_colour
        self.title = title


    def run(self):
  
        # Define the dimensions of
        # screen object(width,height)
        screen = pygame.display.set_mode((self.width, self.height))
    
        
        
        # Set the caption of the screen
        pygame.display.set_caption(self.title)

        
        # Fill the background colour to the screen
        screen.fill(self.background_colour)
        
        # Update the display using flip
        pygame.display.flip()
        
        # Variable to keep our game loop running
        running = True
        
        # game loop
        while running:
            
        # for loop through the event queue  
            for event in pygame.event.get():
            
                # Check for QUIT event      
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()
        exit()
                