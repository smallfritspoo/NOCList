# Design Decisions
First and foremost this is not the way that I would approach this problem in the real world. The most immediate
changes would be to ditch the custom logic behind retries and backoff. This is much better accomplished by using
requests plugins, or other context managers with robust mocking options. There is seldom reason to reinvent the wheel,
when others have a more robust and mature wheel for your vehicle.

## NOCList class
Most of the logic is wrapped up into a a NOCList class that handles writing logging messages, and provides a small amount
of obfuscation to methods and attributes related to the retrieved authentication key.

This does increase complexity mildly, however it eases the burden of testing and mocking for tests.

The project also has basic configuration for being imported as a library (again useful for easing the testing requirements)

## Testing mentality
Current testing mentality is basic, and provides little option for individual element testing, however tests the basic
behavior, while providing for reasonable coverage of the run code.


## Helper Files
`run_tests.sh` is provided to allow easy testing. You don't need to bother remembering what python modules or files are 
included or required. The file would also be of use during the implementation of a CI/CD pipeline as it would simplify 
the configuration of those services for running automated testing.