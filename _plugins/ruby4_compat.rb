# Restores Object#tainted? and Object#untaint removed in Ruby 3.2+
# Required for Jekyll 3.9 / Liquid 4.0.3 compatibility with Ruby 4.0
if RUBY_VERSION >= "3.2"
  class Object
    def tainted?
      false
    end

    def untaint
      self
    end
  end
end
