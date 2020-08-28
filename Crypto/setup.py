from cx_Freeze import setup,Executable

setup(
	name        = "crypteur",
	version     = "1",
	description = "crypteur à clé unique",
	executables = [Executable("crypteur.py")]
)