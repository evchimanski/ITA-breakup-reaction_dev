      program brkupdists

      parameter(maxang=90,maxe=100)

      character aa*48,db*8,an(0:9)*1
      dimension sigs(6,maxang,maxe),th(maxang),e1(maxe),e2(maxe)
      dimension sigx(6)

      data an/'0','1','2','3','4','5','6','7','8','9'/ 

      data ird/1/,iwrt/2/

C  File name and file name prep

 10   write(*,*) 'Enter filename (to quit, enter stop)'
      read(*,'(a48)') aa
      if(aa(1:4).eq.'stop') stop

      do i=48,1,-1
        if(aa(i:i).eq.'.') lst=i
       end do
      lst=lst-1

      if(lst.eq.0) then
        write(*,*) 'No filename given.'
        stop
       endif

      open(unit=ird,file=aa, status='old')
      open(unit=iwrt,file=aa(1:lst)//'.dat', status='unknown')

C Read distributions

      ne=0

 20   read(ird,'(a8)',end=40) db
      if(db.ne.'   Ed=  ') go to 20

      ne=ne+1
      nth=0
      read(ird,'(6x,f12.4,13x,f12.4,14x,f12.4)') e1(ne)
      read(ird,'(6x,f12.4,13x,f12.4,14x,f12.4)') e2(ne)
      !print*, e1(ne)
      !pause

c      do i=1,4
c      do i=1,7
c        read(ird,*)
c       end do
 25   read(ird,'(a8)') db
      if(db.ne.'      th') go to 25

 30   nth=nth+1
      read(ird,'(f12.4,2(2x,3e15.4))') th(nth),(sigs(i,nth,ne),i=1,6)
      
      
      if(sigs(3,nth,ne).gt.0.0) go to 30
      go to 20

C Write desired distributions

 40   nth=nth-1

 50   write(*,*) 'Enter 1 for ang. distribution at fixed E1'
      write(*,*) '      2 for spectrum at fixed angle'
      read(*,*) iea
      if(iea.gt.2 .or. iea.lt.1) go to 80

      if(iea.eq.1) then

c angular distribution for fixed e1

 60     write(*,*) 'Enter energy e1x'
        read(*,*) e1x
        if(e1x.lt.0.0) go to 50

        if(e1x.lt.e1(1) .or. e1x.gt.e1(ne)) then
           write(*,*) 'e1x out of range!'
           go to 60
          endif

        nf2=e1x+0.1
        nf1=nf2/10
        nf2=nf2-10*nf1
        aa(lst+1:lst+4)='-e'//an(nf1)//an(nf2) 
        open(unit=iwrt,file=aa(1:lst+4)//'.dat', status='unknown')

        nx1=(ne-1)*(e1x-e1(1))/(e1(ne)-e1(1))+1
        if(nx1.lt.1) nx1=1
        if(e1x.lt.e1(nx1)) nx1=min(nx1+1,ne-2)
        e2x=e1(1)+e2(1)-e1x
        write(*,*) nx1,e1(nx1),e1x,e2x

        do mth=1,nth
          do i=1,6
           ds=log(sigs(i,mth,nx1+1)/sigs(i,mth,nx1))/(e1(nx1+1)-e1(nx1))
           dds=log(sigs(i,mth,nx1+2)/sigs(i,mth,nx1+1))
     1                                            /(e1(nx1+2)-e1(nx1+1))
           dds=(dds-ds)/(e1(nx1+2)-e1(nx1))
           sigx(i)=log(sigs(i,mth,nx1))+(e1x-e1(nx1))*
     1                                     (ds+(e1x-e1(nx1+1))*dds)
           sigx(i)=exp(sigx(i))
          end do
          write(iwrt,'(9f12.4)') th(mth),e1x,e2x,
     1                                     (sigx(i),i=1,6)
         end do
        close(iwrt)
        go to 60

       else

 70     write(*,*) 'Enter angle thx'
        read(*,*) thx
        if(thx.lt.0.0) go to 50
        
           
        if(thx.lt.th(1) .or. thx.gt.th(nth)) then
           write(*,*) 'thx out of range!'
           go to 70
          endif

        nf2=thx+0.1
        nf0=nf2/100
        nf2=nf2-100*nf0
        nf1=nf2/10
        nf2=nf2-10*nf1
        aa(lst+1:lst+5)='-a'//an(nf0)//an(nf1)//an(nf2) 
        open(unit=iwrt,file=aa(1:lst+5)//'.dat', status='unknown')
         
        
         
         
        do k=1, nth
         if(thx.eq.th(k)) then 
         print*, 'igual', thx,'=',th(k), 'ntheta=', k  
            do me=1,ne 
c                   !write(*,*) me,thx,e1(me),e2(me),
c     1                                     (sigs(i,k,me),i=1,6)
               write(iwrt,*) thx,e1(me),e2(me),(sigs(i,k,me),i=1,6)
           
            enddo
            close(iwrt)
            go to 70 
           endif
           enddo     
         
        nt=(nth-1)*(thx-th(1))/(th(nth)-th(1))+1
        if(nt.lt.1) nt=1
        if(thx.lt.th(nt)) nt=min(nt+1,nth-2)
        write(*,*) nt,th(nt),thx

        do me=1,ne
          do i=1,6
            ds=log(sigs(i,nt+1,me)/sigs(i,nt,me))/(th(nt+1)-th(nt))
            dds=log(sigs(i,nt+2,me)/sigs(i,nt+1,me))
     1                                           /(th(nt+2)-th(nt+1))
            dds=(dds-ds)/(th(nt+2)-th(nt))
            sigx(i)=log(sigs(i,nt,me))+(thx-th(nt))*
     1                                     (ds+(thx-th(nt+1))*dds)
            sigx(i)=exp(sigx(i))
            
      ! print*, thx, nt  ,log(sigs(i,nt+2,me)/sigs(i,nt+1,me))
            
           end do
                 
          write(iwrt,'(9f12.4)') thx,e1(me),e2(me),
     1                                     (sigx(i),i=1,6)
         end do
        close(iwrt)
        go to 70

       endif

 80   close(ird)

      go to 10

      end
