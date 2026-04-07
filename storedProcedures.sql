--INSTRUCTOR CRUD

--Instructor Create

CREATE PROCEDURE createInstructor (
IN pID VARCHAR(5),
IN pName VARCHAR(20),
IN pDept_name VARCHAR(20),
IN pSalary DECIMAL(8,2)
)
BEGIN
    INSERT INTO instructor (ID, name, dept_name, salary)
    VALUES (pID, pName, pDept_name, pSalary);
END


--Instructor Read

CREATE PROCEDURE findInstructor (
    In pID VARCHAR(5)
)
BEGIN
    select from instructor
    where instructor.ID = pID;
END

--Instructor Update

CREATE PROCEDURE updateInstructorName ()

CREATE PROCEDURE updateInstructorSalary ()

CREATE PROCEDURE updateInstructorDept ()


--Instructor Delete

CREATE PROCEDURE deleteInstructor (
    In pID VARCHAR(5)
)
BEGIN
    delete from instructor
    where instructor.ID = pID;
END

--STUDENT CRUD


--Student Create

CREATE PROCEDURE createStudent (
IN pID VARCHAR(5),
IN pName VARCHAR(20),
IN pDept_name VARCHAR(20),
IN pTot_cred DECIMAL(3,0)
)
BEGIN
    INSERT INTO student (ID, name, dept_name, tot_cred)
    VALUES (pID, pName, pDept_name, pTot_cred);
END

--Student Read

CREATE PROCEDURE findStudent (
    In pID VARCHAR(5)
)
BEGIN
    select from instructor
    where student.ID = pID;
END

--Student Update

CREATE PROCEDURE updateStudentName ()

CREATE PROCEDURE updateStudentDept ()

CREATE PROCEDURE updateStudentCredit ()

--Student Delete

CREATE PROCEDURE deleteStudent (
    In pID VARCHAR(5)
)
BEGIN
    delete from student
    where student.ID = pID;
END

--SECTION CRUD


--Section Create

CREATE PROCEDURE createSection (
IN pCourse_id VARCHAR(8),
IN pSec_id VARCHAR(8),
IN pSemester VARCHAR(6),
IN pYear DECIMAL(4,0)
IN pBuilding VARCHAR(15),
IN pRoom_number VARCHAR(7),
IN pTime_slot_id VARCHAR(4)
)
BEGIN
    INSERT INTO section (course_id, sec_id, semester, year, building, room_number, time_slot_id)
    VALUES (pCourse_id, pSec_id, pSemester, pYear, pBuilding, pRoom_number, pTime_slot_id);
END


--Section Read

CREATE PROCEDURE findSection ()

--Section Update

CREATE PROCEDURE updateSectionBuilding ()

CREATE PROCEDURE updateSectionRoomNumber ()

CREATE PROCEDURE updateTimeSlotId ()

--Section Delete

CREATE PROCEDURE deleteSection (
    In pSec_id VARCHAR(5)
)
BEGIN
    delete from section
    where section.sec_id = pSec_id;
END

--Enroll in a Class

CREATE PROCEDURE classEnroll ()

--Assign Instructor to Class

CREATE PROCEDURE assignInstructor ()

--Drop a Section

CREATE PROCEDURE dropSection ()

--Give a Grade to a Section

CREATE PROCEDURE gradeSection ()