function katz(A :: Array{Int64,2}, α :: Float64, β :: Float64)
  n, _ = size(A)
  e = ones(n)
  last = copy(e)
  for _ in 1:50
    current = α * A * last + β * e
    last = copy(current)
  end
  return last
end

begin
    A = [0 1 1 1 0; 1 0 1 1 1; 1 1 0 1 1; 1 1 1 0 0; 0 1 1 0 0]
    score = katz(A, 0.25, 0.2)
    println(score)
end