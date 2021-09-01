# typed: strict
module TypedParams
  extend T::Generic

  Elem = type_member

  sig { params(args: Parlour::Types::Proc::Parameter, raise_coercion_error: T.nilable(T::Boolean)).returns(Elem) }
  def extract!(args, raise_coercion_error: nil); end
end
