import goodboysimworld

def main():
	world = goodboysimworld.simworld()
	world.init_screen()
	world.load_world()
	world.run()

if __name__ == "__main__":
	main()