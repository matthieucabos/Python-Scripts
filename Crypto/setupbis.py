from cx_Freeze import setup,Executable

setup(
	name        = "decrypteur",
	version     = "1",
	description = "decrypteur à clé unique",
	executables = [Executable("resolveur.py")]
)