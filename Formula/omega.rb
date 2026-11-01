class Omega < Formula
  desc "AI-driven macOS maintenance: updates like topgrade, cleans like Mole"
  homepage "https://github.com/lcajigasm/omega"
  license "MIT"

  head do
    url "https://github.com/lcajigasm/omega.git", branch: "main"

    depends_on "go" => :build
  end

  # Stable URLs and sha256 lines are rewritten by .github/scripts/update-formula.py.
  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/lcajigasm/omega/releases/download/v0.10.0/omega_0.10.0_darwin_arm64.tar.gz"
      sha256 "e07c80c5c6057be3c3acd18632239a0110ebf0d74bcb517ce92f1551ea6f48bf"
    end
    if Hardware::CPU.intel?
      url "https://github.com/lcajigasm/omega/releases/download/v0.10.0/omega_0.10.0_darwin_amd64.tar.gz"
      sha256 "927886263140a1d8f51746e7cfbcb2718a84899ac8deaf1da7f6a40e18be090b"
    end
  end

  on_linux do
    if Hardware::CPU.arm? && Hardware::CPU.is_64_bit?
      url "https://github.com/lcajigasm/omega/releases/download/v0.10.0/omega_0.10.0_linux_arm64.tar.gz"
      sha256 "d1c4c131e44376dae208d60e36a7052d5cd020c404884077042cd25280c75ddf"
    end
    if Hardware::CPU.intel? && Hardware::CPU.is_64_bit?
      url "https://github.com/lcajigasm/omega/releases/download/v0.10.0/omega_0.10.0_linux_amd64.tar.gz"
      sha256 "5ca846181a3d93da63b58754566ee9af4bf5066ca944b2bd848eaabb3b8c4d26"
    end
  end

  def install
    if build.head?
      system "go", "build", *std_go_args(ldflags: "-s -w -X main.version=#{version}"), "./cmd/omega"
    else
      bin.install "omega"
    end
    generate_completions_from_executable(bin/"omega", shell_parameter_format: :cobra)
  end

  def caveats
    <<~EOS
      Configure a provider and API key with:
        omega setup
      topgrade and Mole are optional backends:
        brew install topgrade mole
    EOS
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/omega --version")
    assert_match "brew", shell_output("#{bin}/omega steps")
  end
end
