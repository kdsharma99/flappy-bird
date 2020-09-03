import cx_Freeze
executables=[cx_Freeze.Executable("flappybird.py")]
cx_Freeze.setup(name="Snake Game by Kushal Sharma",
options={"build_exe":{"packages":["pygame"],
"include_files":["0.png","1.png","2.png","3.png","4.png","5.png","6.png","7.png","8.png","9.png","game_over.jpg",
"Highscore.txt","cartoon_city.jpg","gameover.mp3","base.png","bird.png","background.png","die.wav","hit.wav","pipe.png","point.wav","swoosh.wav","wing.wav"]}},
executables=executables
)
