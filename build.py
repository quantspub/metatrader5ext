# import os
# import shutil
# import sys
# import numpy as np
# from pathlib import Path
# import platform
# import tomllib
# import datetime as dt
# from Cython.Compiler import Options
# from Cython.Build import build_ext, cythonize
# from setuptools import Distribution, Extension

# # Configuration flags
# PROFILE_MODE = bool(os.getenv("PROFILE_MODE", ""))
# ANNOTATION_MODE = bool(os.getenv("ANNOTATION_MODE", ""))

# # Build directory
# if PROFILE_MODE:
#     BUILD_DIR = None
# elif ANNOTATION_MODE:
#     BUILD_DIR = "build/annotated"
# else:
#     BUILD_DIR = "build/optimized"

# # Cython compiler options
# Options.docstrings = True
# Options.fast_fail = True
# Options.annotate = ANNOTATION_MODE
# Options.warning_errors = True
# Options.extra_warnings = True

# CYTHON_COMPILER_DIRECTIVES = {
#     "language_level": "3",
#     "cdivision": True,
#     "nonecheck": True,
#     "embedsignature": True,
#     "profile": PROFILE_MODE,
#     "linetrace": PROFILE_MODE,
#     "warn.maybe_uninitialized": True,
# }

# compile_args = ["-O3"]
# link_args = []
# include_dirs = [np.get_include()]
# libraries = ["m"]


# def build_extensions() -> list[Extension]:
#     define_macros = [("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]
#     if PROFILE_MODE or ANNOTATION_MODE:
#         define_macros.append(("CYTHON_TRACE", "1"))

#     extra_compile_args = []
#     if platform.system() != "Windows":
#         extra_compile_args.append("-Wno-unreachable-code")
#         if not PROFILE_MODE:
#             extra_compile_args.extend(["-O3", "-pipe"])

#     # Get the Cython include directory manually
#     # cython_include = (
#     #     Path(Options.get_include())
#     #     if hasattr(Options, "get_include")
#     #     else Path("build")
#     # )

#     return [
#         Extension(
#             name=str(pyx.relative_to(".")).replace(os.path.sep, ".")[:-4],
#             sources=[str(pyx)],
#             include_dirs=[np.get_include()],
#             # include_dirs=[np.get_include(), cython_include.__str__()],
#             define_macros=define_macros,
#             language="c",
#             extra_compile_args=extra_compile_args,
#         )
#         for pyx in Path("metatrader5ext").rglob("*.pyx")
#     ]


# def copy_build_to_source(cmd) -> None:
#     for output in cmd.get_outputs():
#         relative_extension = Path(output).relative_to(cmd.build_lib)
#         if Path(output).exists():
#             shutil.copyfile(output, relative_extension)
#             mode = relative_extension.stat().st_mode
#             mode |= (mode & 0o444) >> 2
#             relative_extension.chmod(mode)
#     print("Copied all compiled dynamic library files into the source directory")


# def build() -> None:
#     extensions = build_extensions()
#     if not extensions:
#         raise ValueError(
#             "No extensions found to build. Ensure .pyx files are in the correct location."
#         )

#     ext_modules = cythonize(
#         extensions,
#         compiler_directives=CYTHON_COMPILER_DIRECTIVES,
#         nthreads=os.cpu_count(),
#         build_dir=BUILD_DIR,
#     )
#     if not ext_modules:
#         raise ValueError("Cythonize returned no extensions. Check your configurations.")

#     distribution = Distribution(
#         {
#             "name": "metatrader5ext",
#             "ext_modules": ext_modules,
#             "zip_safe": False,
#         }
#     )
    
#     cmd = distribution.get_command_obj("build_ext")
#     cmd.inplace = True
#     if not getattr(cmd, "extensions", None):
#         cmd.extensions = ext_modules  # Fallback to manually set extensions
        
#     cmd.ensure_finalized()
#     cmd.cython_include_dirs = cmd.cython_include_dirs or [] 
#     cmd.run()

#     copy_build_to_source(cmd)


# if __name__ == "__main__":
#     with open("pyproject.toml", "rb") as f:
#         pyproject_data = tomllib.load(f)
#     project_version = pyproject_data["tool"]["poetry"]["version"]
#     print("\033[36m")
#     print("=====================================================================")
#     print(f"MetaTrader5Ext Builder {project_version}")
#     print(
#         "=====================================================================\033[0m"
#     )
#     print(f"System: {platform.system()} {platform.machine()}")
#     print(f"Python: {platform.python_version()} ({sys.executable})")
#     print(f"Cython: {np.__version__}")

#     print(f"\nPROFILE_MODE={PROFILE_MODE}")
#     print(f"ANNOTATION_MODE={ANNOTATION_MODE}")
#     print(f"BUILD_DIR={BUILD_DIR}")
#     print("\nStarting build...")
#     ts_start = dt.datetime.now(dt.timezone.utc)
#     build()
#     print(f"Build time: {dt.datetime.now(dt.timezone.utc) - ts_start}")
#     print("\033[32m" + "Build completed" + "\033[0m")
