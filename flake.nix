{
  # May not be the most "nix" way to accomplish this, but works for now.
  description = "Basic interpysh flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { nixpkgs, ... }:
  let system = "x86_64-linux"; pkgs = import nixpkgs { system = "${system}"; config.allowUnfree = true; }; in
  {
    devShells."${system}".default =
      pkgs.mkShellNoCC {
        buildInputs = [ pkgs.bashInteractive ];
        packages = with pkgs; [
          python311
          python311Packages.pip
          (vscode-with-extensions.override {
            vscodeExtensions = with vscode-extensions; [
              ms-python.python
              ms-python.vscode-pylance
            ];
          })
        ];
        shellHook = ''
          export SHELL=${pkgs.lib.getExe pkgs.bashInteractive}
          python -m venv .venv
          source .venv/bin/activate
          pip install -r requirements.txt
          pip install -e .
        '';
      };
  };
}

