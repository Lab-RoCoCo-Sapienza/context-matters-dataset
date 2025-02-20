(define (domain other-domain)

    (:requirements
        :strips
        :typing
    )

    (:types
        room locatable - object
        robot grabbable container - locatable
        
    )

    (:predicates
        (at ?something - locatable ?where - room)
        (is-holding ?who - robot ?something - grabbable)
        (is-free ?who - robot)
        (is-inside ?what - grabbable ?where - container)
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
    
    (:action put_inside
        :parameters (?who - robot ?what - grabbable ?inside - container ?where - room)
        :precondition (and (at ?who ?where)(at ?inside ?where)(is-holding ?who ?what))
        :effect (and (not (is-holding ?who ?what))(is-inside ?what ?inside)(is-free ?who))
    )
    
    (:action extract_from
        :parameters (?who - robot ?what - grabbable ?inside - container ?where - room)
        :precondition (and (at ?who ?where) (at ?inside ?where) (is-inside ?what ?inside) (is-free ?who))
        :effect (and (not (is-inside ?what ?inside)) (is-holding ?who ?what) (not (is-free ?who)))
    )
)