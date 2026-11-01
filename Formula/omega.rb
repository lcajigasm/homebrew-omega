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
      url "https://github.com/lcajigasm/omega/releases/download/v0.11.0/omega_0.11.0_darwin_arm64.tar.gz"
      sha256 "fc279464337732d3bc1d4eee05b761696ac410900dba21d47ef608f46a90b2c8"
    end
    if Hardware::CPU.intel?
      url "https://github.com/lcajigasm/omega/releases/download/v0.11.0/omega_0.11.0_darwin_amd64.tar.gz"
      sha256 "4ed103ee4b9277b79705722df2ca8ae03481c85ddedfe2c1db759a2fc5e61a68"
    end
  end

  on_linux do
    if Hardware::CPU.arm? && Hardware::CPU.is_64_bit?
      url "https://github.com/lcajigasm/omega/releases/download/v0.11.0/omega_0.11.0_linux_arm64.tar.gz"
      sha256 "9165b46b3702f9f3332e77f5ff0d11b36b5955e80367599b6c11c0f8da495f23"
    end
    if Hardware::CPU.intel? && Hardware::CPU.is_64_bit?
      url "https://github.com/lcajigasm/omega/releases/download/v0.11.0/omega_0.11.0_linux_amd64.tar.gz"
      sha256 "bf206a98d8d635cfc623f052eb353b9a440b18d6357159056381e51bf6adeb6e"
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
