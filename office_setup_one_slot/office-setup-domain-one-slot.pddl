(define (domain office-setup-domain)

    (:requirements
        :strips
        :typing
        :negative-preconditions
        :derived-predicates
    )

    (:types
        room locatable - object
        robot grabbable movable - locatable
    )

    (:predicates
        (at ?something - locatable ?where - room)
        (is-holding ?who - robot ?something - grabbable)
        (is-free ?who - robot)
        (inside ?what - object ?where - movable)
        (slot-free ?what - movable)
    )

    (:action move_to
        :parameters (?who - robot ?from - room ?to - room)
        :precondition (and (at ?who ?from))
        :effect (and (not (at ?who ?from)) (at ?who ?to))
    )
    
    (:action grab
        :parameters (?who - robot ?what - grabbable ?where - room)
        :precondition (and (at ?who ?where) (is-free ?who))
        :effect (and 
                    (not (at ?what ?where)) 
                    (is-holding ?who ?what) 
                    (not (is-free ?who))
                )
    )

    (:action drop
        :parameters (?who - robot ?what - grabbable ?where - room)
        :precondition (and 
                        (at ?who ?where) 
                        (is-holding ?who ?what)
                    )
        :effect (and 
                    (not (is-holding ?who ?what)) 
                    (is-free ?who) 
                    (at ?what ?where)
                )
    )

    (:action push
        :parameters (?who - robot ?what - movable ?contained_item - object ?from - room ?to - room )
        :precondition (and 
                        (at ?who ?from)
                        (at ?what ?from)
                        (slot-free ?what)
                        (inside ?contained_item ?what)
                    )
        :effect (and 
                    (not (at ?who ?from)) 
                    (not (at ?what ?from))
                    (at ?who ?to) 
                    (at ?what ?to)    
                    (at ?contained_item ?to)
                )
    )

    (:action put_inside
        :parameters (?who - robot ?what - grabbable ?where - movable ?room - room)
        :precondition (and 
                            (at ?who ?room) 
                            (at ?where ?room) 
                            (is-holding ?who ?what)
                            (slot-free ?where)
                        )
        :effect (and 
                    (inside ?what ?where) 
                    (not (is-holding ?who ?what)) 
                    (is-free ?who)
                    (not (slot-free ?where))
                )
    )

    (:action remove_from
        :parameters (?who - robot ?what - grabbable ?in - movable ?where - room)
        :precondition (and 
                        (at ?who ?where) 
                        (at ?in ?where) 
                        (inside ?what ?in) 
                        (is-free ?who)
                    )
        
        :effect (and 
                    (not (inside ?what ?in)) 
                    (is-holding ?who ?what) 
                    (not (is-free ?who))
                    (slot-free ?in)
                )
    )
)