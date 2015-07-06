class DeteriorateClothes

	def initialize
	end

	def process
		return false unless @running

		items = [df.world.items.other[:GLOVES], 
				 df.world.items.other[:ARMOR], 
				 df.world.items.other[:SHOES], 
				 df.world.items.other[:PANTS], 
				 df.world.items.other[:HELM]]
				 
		items.each { |type|
			type.each { |i|
				if (i.subtype.armorlevel == 0 and i.flags.on_ground == true and i.wear > 0)
					i.wear_timer *= i.wear + 0.5
					if (i.wear > 2)
						i.flags.garbage_collect = true
					end					
				end
			}			
		}
		
		
	end
	
	def start
		@onupdate = df.onupdate_register('deteriorateclothes', 1200, 1200) { process }
		@running = true
		
		puts "Deterioration of old clothes commencing..."
		
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
	if ($DeteriorateClothes)
		$DeteriorateClothes.stop
	end
	
    $DeteriorateClothes = DeteriorateClothes.new
    $DeteriorateClothes.start

when 'end', 'stop'
    $DeteriorateClothes.stop
	
else
    if $DeteriorateClothes
        puts $DeteriorateClothes.status
    else
        puts 'Not loaded.'
    end
end