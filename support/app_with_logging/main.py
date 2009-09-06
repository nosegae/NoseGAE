import wsgiref.handlers
from helloworld import application
        
def main():
    wsgiref.handlers.CGIHandler().run(application())

if __name__ == '__main__':
    main()
