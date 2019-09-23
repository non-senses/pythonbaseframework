# Best Practices

* Group elements as per the following rule:
> Things that change at the same time or for the same reasons remain together. Things that change at different times or for different reasons are separated.

* Reduce the number of function arguments to the minimum
    * Zero arguments is the best.
    * One argument works, as long as the argument is not a `boolean`.
    * Two arguments are acceptable if justified.
    * Three arguments should be avoided where possible.
    * More than three, you'll need to have a very good explaination.
        * Most probably you should be passing a DTO instead.
    


# The application structure

* Create modules per business epics.
* Upon any required change, the tickets should be split in such a way that only one business module or directory has changes.
* The `infrastructure` module belongs to the Tech Team, as it module enables the business part of the application to interact with the infrastucture we've set in place.
* External services are grouped in a single module named `external`; where we may split them again by domain.
* A module contains all the elements required to fulfill the business need, regardless of the role.
    * Good: group controllers, services, models, etc. into a single module.
    * Bad: distribute a single module into roles buckets, such as `controllers`, `gateways`, `models`, etc.
    * Question: where do the tests go?


# Key concepts:

## The controllers are the application single entry points

* The only, single entrypoint of the application on what comes down to _do business actions_ is the controllers. Any kind of business task will start as a response to an application-level event.

An event is not a PubSub event -that is an event _notification_.
An event is something that ocurrs in your application. 

- Receiving a web-request is an event, normally handled by the @routes
- Receiving a SIGHUP signal is an event, normally handled by the `process` object, ie: `process.on('SIGHUP', () => { console.log('Received signal SIGHUP')})`
- Receiving a message from a message queue, ie through SQS


This means that there should not exist any special script that calls any special function to do anything related to business.

* The only, single entrypoint on what comes down to _do business actions_ is the controller.
    * The reason is that we should be able to explain the controller to the Product Manager.


## The controllers use the services to achieve the task
* The service function names should:
    * be clear to the Project Manager. 
    * consist of a verb, be descriptive and possibly include some context, for example:
        * `extract_msrps_from_product_payload` and `persist_base_price_candidate` are good examples, even more when you know the names of the parameters
        * `compute`, `process`, `generate` and similar are bad examples, as it is not clear what these functions do.
* The module-specific service will rely on other services that belong to 2 external modules:
    * Infrastructure, to use Mongo, SQS, cache, etc.
    * ExternalServices, to interact with external services such as Ms-Tax, HQM, SAP, etc.




# Python tricks
* Still not sure on how to set up the debugger in Visual Studio Code
* Due to memory constraints, many libraries might return a `generator` instead of a `collection`.
    * Generators are not a Python specific thing, but are more used in Python due to the data-science approach of the language.
    * Generators are exhausted once they are consumed, so only one consumption can happen.
    * Looping through a generator will consume the generator, thus it will be empty right after the loop.
    
# Python specifics
* `enumerate()`
    * Enumerates items over an iterator. `enumerate` provides the counter and iterates over the object passed as parameter by calling the  `__next__()` method on it.
    * ```
teams = ['stash', 'kopi', 'katana']
for item_index, team_name in enumerate(teams):
    print("In the index {OneNamedPlaceholder} you can find the team {AnotherNamedPlaceholder}".format(AnotherNamedPlaceholder=team_name, OneNamedPlaceholder = item_index))

In the index 0 you can find the team stash
In the index 1 you can find the team kopi
In the index 2 you can find the team katana
>>>            
    ```
* dict().items():
    * Builds an iterator from a dictionary.
    * ```
a_dictionary = { 'A' : 'Letter A', 'b':'letter b, lower case', 'B':'Letter B, upper case' }
for key, value in a_dictionary.items():
    print('k {}, v {}'.format(key, value))

k A, v Letter A
k B, v Letter B, upper case
k b, v letter b, lower case
    ```
* Function arguments: position vs named arguments
    * Functions can receive arguments in two ways: position and named.
    * Position arguments: as most programming languages:

```
def my_function(first_argument, second_argument, third_argument):
    if first_argument == second_argument:
        print ("First and second contain the same value: {}".format(second_argument))
    
    if third_argument == second_argument:
        print ("Third and second contain the same value: {}".format(second_argument))

>>> my_function("one","two","three")
>>> my_function("one","two","two")
Third and second contain the same value: two
>>> my_function("one","one","three")
First and second contain the same value: one
>>> my_function("one","one","one")
First and second contain the same value: one
Third and second contain the same value: one
```


* Special `**kwargs`;