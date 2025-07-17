{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python311
    python3
    python3Packages.numpy
    (python311.withPackages (pyPkgs: with pyPkgs; [
      numpy
      opencv
      scikit-learn
      joblib
      psutil
      # Add other Python packages from your requirements.txt here if they are not already provided by Nixpkgs
      # For example:
      # librosa
      # pandas
      # matplotlib
      # pillow
      # jupyter
      # notebook
      # tqdm
      # seaborn
      # pyserial
      # requests
      # av
      # Flask
      # Flask_Toastr
      # gitpython
      # ipython
      # kornia
      # pims
      # PyYAML
      # scipy
      # torch
      # torchvision
      # tensorboard
      # Werkzeug
    ]))
  ];

  # Set environment variables if needed
  shellHook = ''
    echo "Entering Nix-managed development environment"
    # You can add any commands here that should run when entering the shell
  '';
}