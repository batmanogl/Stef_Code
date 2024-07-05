puts ("Welcome, Write me the text you want to cipher:")
message = gets.chomp
puts "Ok, I receive the message!"

puts ("Now please write me the shift factor:")
factor = gets.chomp
puts "Ok, I receive the factor!"
factor = factor.to_i

message_length = message.length
puts (message_length)

for letter in 0..message_length
  puts message[letter]
end