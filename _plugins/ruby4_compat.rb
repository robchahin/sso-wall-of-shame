# Ruby 4.0+ compatibility shim for Jekyll 3.9 / Liquid 4.0.3
# Loaded via RUBYOPT in bin/serve, before bundler isolation is set up.
if RUBY_VERSION >= "3.2"
  # Pre-require gems removed from Ruby stdlib so Jekyll's internal requires
  # find them already loaded and skip them, bypassing bundler isolation.
  %w[csv bigdecimal logger ostruct base64 mutex_m].each do |lib|
    begin
      require lib
    rescue LoadError
      # Not available on this Ruby version, skip
    end
  end

  # Restore Object#tainted? and Object#untaint removed in Ruby 3.2+
  # Required by Liquid 4.0.3 (used by Jekyll 3.9)
  class Object
    def tainted?
      false
    end

    def untaint
      self
    end
  end
end
