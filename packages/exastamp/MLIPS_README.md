# `exastamp +mlips` Spack build — known issues (2026-06-10)

## Symptom

`spack install exastamp+mlips@v3.8.0` fails during the **install** phase
(not configure, not build):

```
-- Installing: /pace/cnpy
CMake Error at src/potential/mlip-pace/pace-mlip/cmake_install.cmake:54 (file):
  file INSTALL cannot make directory "/pace/cnpy": No such file or directory.
make: *** [Makefile:113: install] Error 1
```

The PACE repo clone (done at CMake-configure time by exaStamp's top-level
`CMakeLists.txt`, into `${CMAKE_BINARY_DIR}/external/pace`) succeeds, and
`exaStampPace-plugin.so` builds and links fine. The failure is purely in the
generated install rules for the bundled `cnpy`/`wigner` sub-libs of PACE.

Build log evidence (from
`/tmp/<user>/spack-stage/spack-stage-exastamp-v3.8.0-<hash>/`):
- `spack-configure-args.txt` — shows the cmake invocation flags
- `spack-build-01-cmake-out.txt` — clone happens fine, `Cloning into 'pace'...`
- `spack-build-03-install-out.txt` — the `/pace/cnpy` error above

## Root cause 1 (blocking) — bug in `Collab4exaNBody/exaStamp_mlip_pace`

In that repo's top-level `CMakeLists.txt`:

```cmake
## cnpy (always built from bundled source)
...
install(DIRECTORY cnpy
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/pace   # <-- CMAKE_INSTALL_INCLUDEDIR is empty here!
  FILES_MATCHING PATTERN *.h
)

## wigner-cpp
...
install(DIRECTORY wigner
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/pace   # <-- same problem
  FILES_MATCHING PATTERN *.hpp
)

...
include(GNUInstallDirs)   # <-- only defined here, AFTER the two installs above!
```

`include(GNUInstallDirs)` is called *after* the two `install(DIRECTORY ...)`
calls that already reference `${CMAKE_INSTALL_INCLUDEDIR}`. On a fresh
configure, the variable is undefined/empty, so
`DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/pace` becomes the literal string
`DESTINATION /pace`. CMake treats a destination starting with `/` as an
**absolute path** (filesystem root `/pace`), not as relative to
`CMAKE_INSTALL_PREFIX`. Hence `make install` tries to create `/pace/cnpy`
and fails (no permission / doesn't exist).

### Fix

Move `include(GNUInstallDirs)` to the very top of
`exaStamp_mlip_pace/CMakeLists.txt`, right after `project(libpace ...)`,
before the `install(DIRECTORY cnpy ...)` / `install(DIRECTORY wigner ...)`
calls.

### Why this never showed up in local/manual builds

- `CMAKE_INSTALL_INCLUDEDIR` is a CACHE variable. Once `include(GNUInstallDirs)`
  runs once for a build directory, the value (`include`) is written to
  `CMakeCache.txt` and persists across reconfigures — so on a *reused* local
  `build/` dir, by the time the buggy lines run again, the cache var is
  already set and everything resolves correctly (`include/pace`).
- The bug only manifests in the generated `cmake_install.cmake`, i.e. only
  if `make install` / `cmake --install` actually runs. Plenty of local dev
  workflows just run binaries from the build tree and never install.
- Spack always builds in a brand-new `spack-build-<hash>` directory (empty
  `CMakeCache.txt`) and **always** runs the install step — so the latent
  ordering bug is exposed every time.

## Root cause 2 — bug in `packages/exastamp/package.py` (this repo)

`cmake_args()`:

```python
def cmake_args(self):
    args = [
        self.define_from_variant("EXASTAMP_BUILD_PACE=ON", "mlips" ),
        self.define_from_variant("EXASTAMP_BUILD_POD=ON" , "mlips" ),
    ]
    return args
```

`define_from_variant`'s first argument should just be the CMake variable
name (e.g. `"EXASTAMP_BUILD_PACE"`). As written, Spack's `define()` produces:

```
-DEXASTAMP_BUILD_PACE=ON:BOOL=ON   (when +mlips)
-DEXASTAMP_BUILD_PACE=ON:BOOL=OFF  (when ~mlips)
```

CMake's `-D` parser splits on the *first* `=`, so this sets cache variable
`EXASTAMP_BUILD_PACE` to the **string** `"ON:BOOL=ON"` or `"ON:BOOL=OFF"`.
Neither string is one of CMake's recognized "false" constants
(`0/OFF/NO/FALSE/N/IGNORE/NOTFOUND/""/*-NOTFOUND`), so
`if(EXASTAMP_BUILD_PACE)` evaluates **TRUE in both cases** — i.e. the
`mlips` variant currently has *no effect*: PACE/POD (and the network git
clone of the private PACE repo) are always attempted, even with `~mlips`.

Confirmed in `spack-configure-args.txt`:
```
-DEXASTAMP_BUILD_PACE=ON:BOOL=ON -DEXASTAMP_BUILD_POD=ON:BOOL=ON
```

### Fix

```python
def cmake_args(self):
    return [
        self.define_from_variant("EXASTAMP_BUILD_PACE", "mlips"),
        self.define_from_variant("EXASTAMP_BUILD_POD", "mlips"),
    ]
```

## TODO

- [ ] Fix `include(GNUInstallDirs)` ordering in `exaStamp_mlip_pace/CMakeLists.txt`
- [ ] Fix `define_from_variant` calls in `packages/exastamp/package.py`
- [ ] Re-run `spack install exastamp+mlips@v3.8.0` end to end
- [ ] Consider `~mlips` build too, to confirm it now actually skips PACE/POD
      (and the SSH git clone of `exaStamp_mlip_pace`)
