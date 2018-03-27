from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.db import connection #sql
from django.urls import reverse #used for namespaces
from django.views.decorators.csrf import csrf_exempt #YIKES
from home.forms import *

# Create your views here.

class HomeView(TemplateView):
    template_name = "home/homepage.html"



    def get(self, request):
        #sql query's here to get all info and put into args (temp)
        #TODO: THIS QUERY IS TEMPORARY FOR A TEST, NEEDS TO BE CLEANED UP WITH SORTS, ORGANIZED ARGS, ETC!!!

        # find session corresponding to users enrolled ClassOfSession
        cursor = connection.cursor()
        cursor.execute("SELECT      home_studysession.start_time, \
                                    home_studysession.end_time, \
                                    home_studysession.date, \
                                    home_studysession.building, \
                                    home_studysession.room_number, \
                                    home_studysession.description, \
                                    home_classes.class_code, \
                                    home_classes.class_name, \
                                    home_sessionhas.is_owner, \
                                    home_sessionhas.seshID \
                        FROM        auth_user, \
                                    accounts_enrolledin, \
                                    home_classes, \
                                    home_classofsession, \
                                    home_studysession, \
                                    home_sessionhas \
                        WHERE       accounts_enrolledin.netID = %s AND \
                                    accounts_enrolledin.class_code = home_classes.class_code AND \
                                    home_classes.class_code = home_classofsession.class_code AND \
                                    home_classofsession.seshID = home_studysession.seshID AND \
                                    home_classofsession.seshID = home_sessionhas.seshID \
                        ORDER BY    home_studysession.start_time", [str(request.user)])

        sessions_arr = cursor.fetchall()

        #reorganize queryset to dict
        sessions = []
        for i in range(len(sessions_arr)):
            sessions.append({})
            sessions[i]['start_time'] = sessions_arr[i][0]
            sessions[i]['end_time'] = sessions_arr[i][1]
            sessions[i]['date'] = sessions_arr[i][2]
            sessions[i]['building'] = sessions_arr[i][3]
            sessions[i]['room_number'] = sessions_arr[i][4]
            sessions[i]['description'] = sessions_arr[i][5]
            sessions[i]['class_code'] = sessions_arr[i][6]
            sessions[i]['class_name'] = sessions_arr[i][7]
            sessions[i]['is_owner'] = sessions_arr[i][8]
            sessions[i]['seshID'] = sessions_arr[i][9]

        # find classes user is enrolled in
        cursor.execute("SELECT DISTINCT  accounts_enrolledin.class_code \
                        FROM             auth_user, \
                                         accounts_enrolledin, \
                                         home_classes \
                        WHERE            auth_user.username = accounts_enrolledin.netID")

        #reorganize queryset to dict
        enrolledin_arr = cursor.fetchall()
        enrolledin = []
        for i in range(len(enrolledin_arr)):
            enrolledin.append({})
            enrolledin[i]['auth_user'] = enrolledin_arr[i][0]

        connection.close()

        args = {'sessions': sessions, 'enrolledin': enrolledin}
        return render(request, self.template_name, args)

    @csrf_exempt
    def post(self, request):

        print(request.POST)
        seshID = ""
        if "delete" in request.POST.keys():
            seshID = request.POST["delete"]
        elif "edit" in request.POST.keys():
            seshID = request.POST["edit"]

        cursor = connection.cursor()
        cursor.execute("SELECT           home_sessionhas.netID  \
                        FROM             home_sessionhas \
                        WHERE            home_sessionhas.netID = %s AND\
                                         home_sessionhas.is_owner = 1 AND \
                                         home_sessionhas.seshID = %s", [str(request.user), seshID])


        is_valid_delete = cursor.fetchall()

        if is_valid_delete:
            #DELETE
            if "delete" in request.POST.keys():
                cursor.execute("DELETE FROM      home_studysession \
                                WHERE            home_studysession.seshID = %s", [seshID])
                cursor.execute("DELETE FROM      home_sessionhas \
                                WHERE            home_sessionhas.seshID =  %s", [seshID])
                cursor.execute("DELETE FROM      home_classofsession \
                                WHERE            home_classofsession.seshID = %s", [seshID])

                #GET REQUEST
                # find session corresponding to users enrolled ClassOfSession
                cursor.execute("SELECT      home_studysession.start_time, \
                                            home_studysession.end_time, \
                                            home_studysession.date, \
                                            home_studysession.building, \
                                            home_studysession.room_number, \
                                            home_studysession.description, \
                                            home_classes.class_code, \
                                            home_classes.class_name, \
                                            home_sessionhas.is_owner, \
                                            home_sessionhas.seshID \
                                FROM        auth_user, \
                                            accounts_enrolledin, \
                                            home_classes, \
                                            home_classofsession, \
                                            home_studysession, \
                                            home_sessionhas \
                                WHERE       auth_user.username = accounts_enrolledin.netID AND \
                                            accounts_enrolledin.class_code = home_classes.class_code AND \
                                            home_classes.class_code = home_classofsession.class_code AND \
                                            home_classofsession.seshID = home_studysession.seshID AND \
                                            home_classofsession.seshID = home_sessionhas.seshID \
                                ORDER BY    home_studysession.start_time")

                sessions_arr = cursor.fetchall()

                #reorganize queryset to dict
                sessions = []
                for i in range(len(sessions_arr)):
                    sessions.append({})
                    sessions[i]['start_time'] = sessions_arr[i][0]
                    sessions[i]['end_time'] = sessions_arr[i][1]
                    sessions[i]['date'] = sessions_arr[i][2]
                    sessions[i]['building'] = sessions_arr[i][3]
                    sessions[i]['room_number'] = sessions_arr[i][4]
                    sessions[i]['description'] = sessions_arr[i][5]
                    sessions[i]['class_code'] = sessions_arr[i][6]
                    sessions[i]['class_name'] = sessions_arr[i][7]
                    sessions[i]['is_owner'] = sessions_arr[i][8]
                    sessions[i]['seshID'] = sessions_arr[i][9]

                # find classes user is enrolled in
                cursor.execute("SELECT DISTINCT  accounts_enrolledin.class_code \
                                FROM             auth_user, \
                                                 accounts_enrolledin, \
                                                 home_classes \
                                WHERE            auth_user.username = accounts_enrolledin.netID")

                #reorganize queryset to dict
                enrolledin_arr = cursor.fetchall()
                enrolledin = []
                for i in range(len(enrolledin_arr)):
                    enrolledin.append({})
                    enrolledin[i]['auth_user'] = enrolledin_arr[i][0]

                connection.close()

                args = {'sessions': sessions, 'enrolledin': enrolledin}
                return render(request, self.template_name, args)

            #EDIT
            elif "edit" in request.POST.keys():
                # editSession = NewSessionForm()
                # #get data about selected session
                # cursor.execute("SELECT      home_studysession.start_time, \
                #                             home_studysession.end_time, \
                #                             home_studysession.date, \
                #                             home_studysession.building, \
                #                             home_studysession.room_number, \
                #                             home_studysession.description, \
                #                             home_classofsession.class_code \
                #                 FROM        home_classofsession, \
                #                             home_studysession \
                #                 WHERE       home_classofsession.seshID = %s AND \
                #                             home_studysession.seshID = %s", [seshID, seshID])
                #
                # old_session_sql = cursor.fetchall()
                # #print(old_session_sql)
                # old_session_data = {}
                # old_session_data["start_time"] = old_session_sql[0][0]
                # old_session_data["end_time"] = old_session_sql[0][1]
                # old_session_data["date"] = old_session_sql[0][2]
                # old_session_data["building"] = old_session_sql[0][3]
                # old_session_data["room_number"] = old_session_sql[0][4]
                # old_session_data["description"] = old_session_sql[0][5]
                # old_session_data["enrolled_class"] = old_session_sql[0][6]


                #args = {"form": form}
                connection.close()
                return redirect(reverse('home:edit_session', kwargs={"seshID": seshID}))





class NewSessionView(TemplateView):
    template_name = 'home/new_session.html'

    def get(self, request):
        form = NewSessionForm()
        args = {'form': form}
        return render(request, self.template_name, args)

    def post(self, request):
        form = NewSessionForm(request.POST)

        if form.is_valid(): #override is_valid later for more restriction
            #sql query here
            form.save(request);
            # StudySession.objects.raw('INSERT INTO  home_studysession(start_time,
            #                                        end_time,
            #                                        date,
            #                                        building,
            #                                        room_number,
            #                                        description) \
            #                           VALUES       auth_user, \
            #                                        accounts_enrolledin, \
            #                                        home_classes')

            return redirect(reverse('home:home'))
        else:
            return redirect(reverse('home:new_session')) #deal with fail cases here


class EditSessionView(TemplateView):
    template_name = 'home/edit_session.html'

    def get(self, request, seshID):
        form = EditSessionForm(seshID)
        args = {'form': form}
        return render(request, self.template_name, args)

    def post(self, request, seshID):
        form = EditSessionForm(seshID)

        if form.is_valid(): #override is_valid later for more restriction
            #sql query here
            print(request)
            form.save(request, seshID);
            # StudySession.objects.raw('INSERT INTO  home_studysession(start_time,
            #                                        end_time,
            #                                        date,
            #                                        building,
            #                                        room_number,
            #                                        description) \
            #                           VALUES       auth_user, \
            #                                        accounts_enrolledin, \
            #                                        home_classes')

            return redirect(reverse('home:home'))
        else:
            return redirect(reverse('home:edit_session'), ) #deal with fail cases here
