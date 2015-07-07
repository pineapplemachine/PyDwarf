class DeteriorateCorpses

	def initialize
	end

	def process
		return false unless @running

		df.world.items.other[:ANY_CORPSE].each { |i|
			if (i.flags.dead_dwarf == false)
				i.wear_timer += 1
				if (i.wear_timer > 24 + rand(8))
					i.wear_timer = 0
					i.wear += 1
				end
				if (i.wear > 3)
					i.flags.garbage_collect = true
				end
				
			end
			
		}
		
		df.world.items.other[:REMAINS].each { |i|
			if (i.flags.dead_dwarf == false)
				i.wear_timer += 1
				if (i.wear_timer > 6)
					i.wear_timer = 0
					i.wear += 1
				end
				if (i.wear > 3)
					i.flags.garbage_collect = true
				end
				
			end
			
		}
		
	end
	
	def start
		@onupdate = df.onupdate_register('deterioratecorpses', 1200, 1200) { process }
		@running = true
		
		puts "Deterioration of body parts commencing..."
		
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
	if ($DeteriorateCorpses)
		$DeteriorateCorpses.stop
	end
	
    $DeteriorateCorpses = DeteriorateCorpses.new
    $DeteriorateCorpses.start

when 'end', 'stop'
    $DeteriorateCorpses.stop
	
else
    if $DeteriorateCorpses
        puts $DeteriorateCorpses.status
    else
        puts 'Not loaded.'
    end
end