(define (domain other-domain)

    (:requirements
        :strips
        :typing
    )

    (:types
        room locatable - object
        robot grabbable - locatable
        pc-part accessory - grabbable
    )

    (:predicates
        (at ?something - locatable ?where - room)
        (is-holding ?who - robot ?something - grabbable)
        (is-free ?who - robot)
        (all_different ?p1 - pc-part ?p2 - pc-part ?p3 - pc-part ?p4 - pc-part ?p5 - pc-part ?p6 - pc-part)
        (pc-built)
    )

    (:action move_to
        :parameters (?who - robot ?from - room ?to - room)
        :precondition (and (at ?who ?from))
        :effect (and (not(at ?who ?from))(at ?who ?to))
    )
    
    (:action grab
        :parameters (?who - robot ?what - grabbable ?where - room)
        :precondition (and (at ?who ?where)(at ?what ?where) (is-free ?who))
        :effect (and (not (at ?what ?where))(is-holding ?who ?what)(not(is-free ?who)))
    )
    
    (:action drop
        :parameters (?who - robot ?what - grabbable ?where - room)
        :precondition (and (at ?who ?where)(is-holding ?who ?what))
        :effect (and (not (is-holding ?who ?what)) (is-free ?who) (at ?what ?where))
    )
    
    (:action build-pc
        :parameters (?who - robot ?where - room
                    ?part1 - pc-part ?part2 - pc-part ?part3 - pc-part
                    ?part4 - pc-part ?part5 - pc-part ?part6 - pc-part
                    )
        :precondition (and (at ?who ?where)
            (at ?part1 ?where)(at ?part2 ?where)(at ?part3 ?where)(at ?part4 ?where)(at ?part5 ?where)(at ?part6 ?where)
            (all_different ?part1 ?part2 ?part3 ?part4 ?part5 ?part6)
        )
        :effect (and (pc-built)
            (not(at ?part1 ?where))(not(at ?part2 ?where))(not(at ?part3 ?where))
            (not(at ?part4 ?where))(not(at ?part5 ?where))(not(at ?part6 ?where))
        )
    )
    
)