class DeteriorateFood

	def initialize
	end

	def process
		return false unless @running

		items = [df.world.items.other[:FISH], 
				 df.world.items.other[:FISH_RAW], 
				 df.world.items.other[:EGG], 
				 df.world.items.other[:CHEESE], 
				 df.world.items.other[:PLANT], 
				 df.world.items.other[:PLANT_GROWTH], 
				 df.world.items.other[:FOOD]]
		
		items.each { |type|
			type.each { |i|
				i.wear_timer += 1
				if (i.wear_timer > 24 + rand(8))
					i.wear_timer = 0
					i.wear += 1
				end
				if (i.wear > 3)
					i.flags.garbage_collect = true
				end	
			}
		}
		
		
	end
	
	def start
		@onupdate = df.onupdate_register('deterioratefood', 1200, 1200) { process }
		@running = true
		
		puts "Deterioration of food commencing..."
		
	end
	
	def stop
		df.onupdate_unregister(@onupdate)
		@running = false
	end
	
	def status
		@running ? 'Running.' : 'Stopped.'
	end
		
end	

case $script_args[0]
when 'start'
	if ($DeteriorateFood)
		$DeteriorateFood.stop
	end
	
    $DeteriorateFood = DeteriorateFood.new
    $DeteriorateFood.start

when 'end', 'stop'
    $DeteriorateFood.stop
	
else
    if $DeteriorateFood
        puts $DeteriorateFood.status
    else
        puts 'Not loaded.'
    end
end